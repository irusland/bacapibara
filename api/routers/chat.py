import logging

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from starlette import status
from starlette.responses import RedirectResponse
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import WebSocketException

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.connection.web_socket_connection_manager import WebSocketConnectionManager
from api.models.api.user_credentials import UserCredentials
from api.models.db.user import User
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.interface.users import IUsersStorage
from api.storage.interface.chat import IChatStorage
from api.storage.interface.friends import IFriendsStorage

logger = logging.getLogger(__name__)


def _get_HTML(chat_id: int, user: User) -> str:
    return f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <div>
        <h3>logged in as: {user.name} </h3>
        </div> 
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8000/chat/ws/{chat_id}");
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            }};
            function sendMessage(event) {{
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }}
        </script>
    </body>
</html>
"""


class ChatRouter(APIRouter):
    def __init__(
        self,
        users_storage: IUsersStorage,
        friends_storage: IFriendsStorage,
        jwt_manager: JWTManager,
        jwt_settings: JWTSettings,
        jwt_middleware: JWTMiddleware,
        chat_storage: IChatStorage,
        web_socket_connection_manager: WebSocketConnectionManager,
    ):
        super().__init__()
        self.prefix = "/chat"
        self.tags = [self.prefix]

        @self.post(
            "/start/{friend_id}",
        )
        async def start(
            friend_id: int,
            credentials: UserCredentials = Depends(
                jwt_middleware.get_user_credentials()
            ),
        ):
            user = await users_storage.get_user(credentials.id)
            logger.debug("user %s starting a chat", user)
            friends_ids = await friends_storage.get_friends_for(id=user.id)
            if friend_id not in friends_ids:
                raise HTTPException(
                    status_code=422,
                    detail="Starting a chat with stranger is not allowed",
                )
            chat = await chat_storage.create_chat([user.id, friend_id])
            logger.debug("Started new chat %s", chat)

            return RedirectResponse(
                url=f"/chat/{chat.chat_id}", status_code=status.HTTP_303_SEE_OTHER
            )

        @self.get("/{chat_id}")
        async def get(
            chat_id: int,
            user: User = Depends(jwt_middleware.get_user()),
        ):
            return HTMLResponse(_get_HTML(chat_id=chat_id, user=user))

        @self.websocket("/ws/{chat_id}")
        async def websocket_endpoint(
            websocket: WebSocket,
            chat_id: int,
        ):
            await websocket.accept()

            try:
                user: User = await jwt_middleware.get_user()(websocket)
            except:
                raise WebSocketException("User unauthorized")

            print(f">>> {user=}")
            web_socket_connection_manager.connect(user_id=user.id, websocket=websocket)

            chat = await chat_storage.get_chat(chat_id)

            try:
                while True:
                    data = await websocket.receive_text()
                    await web_socket_connection_manager.broadcast_to_users(
                        chat.user_ids, f"({user.name}): {data}"
                    )
            except WebSocketDisconnect:
                web_socket_connection_manager.disconnect(
                    user_id=user.id, websocket=websocket
                )
                await web_socket_connection_manager.broadcast_to_users(
                    chat.user_ids, f"User ({user.name}) left the chat"
                )
