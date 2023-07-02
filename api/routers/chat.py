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
from api.models.api.chat import Chat
from api.models.api.user_credentials import UserCredentials
from api.models.db.user import User
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.interface.users import IUsersStorage
from api.storage.interface.chat import IChatStorage
from api.storage.interface.friends import IFriendsStorage
from api.storage.message import Message

logger = logging.getLogger(__name__)


def _get_HTML(chat_id: int, user: User) -> str:
    return f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <style>
        ul {{
            max-height: 200px;
            overflow-y: auto;
        }}
        </style>

    </head>
    <body>
        <h1>
          <span>WebSocket Chat by </span>
        </h1>
        <h1>
          <span> by </span>
          <span id="animated-header"> irusland </span>
        </h1>

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
            const messageList = document.getElementById('messages');
            
            function scrollMessageList() {{
                messageList.scrollTop = messageList.scrollHeight;
            }}
            
            messageList.addEventListener('DOMNodeInserted', scrollMessageList);


            const header = document.getElementById("animated-header");
            function generateRainbowPalette(N) {{
              var palette = [];
              var frequency = (2 * Math.PI) / N;
              for (var i = 0; i < N; i++) {{
                var red = Math.round(Math.sin(frequency * i + 0) * 127 + 128);
                var green = Math.round(Math.sin(frequency * i + (2 * Math.PI) / 3) * 127 + 128);
                var blue = Math.round(Math.sin(frequency * i + (4 * Math.PI) / 3) * 127 + 128);
                palette.push(`rgb(${{red}}, ${{green}}, ${{blue}})`);
              }}
              return palette;
            }}

            const colors = generateRainbowPalette(42);

            let shift = 0;
            
            setInterval(() => {{
              let index = 0;
              shift++;
              header.innerHTML = header.textContent.split("").map(letter => {{
                const color = colors[(shift + index++) % colors.length];
                return `<span style="color: ${{color}}">${{letter}}</span>`;
              }}).join("");
              shift = shift % colors.length;
            }}, 50);

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

        async def _load_chat_messages(user_id: int, chat: Chat):
            for message in chat.messages:
                await web_socket_connection_manager.broadcast_to_users(
                    [user_id], message=message
                )

        @self.websocket("/chat/ws/{chat_id}")
        async def websocket_endpoint(
            websocket: WebSocket,
            chat_id: int,
        ):
            await websocket.accept()

            try:
                user: User = await jwt_middleware.get_user()(websocket)
            except:
                raise WebSocketException("User unauthorized")

            web_socket_connection_manager.connect(user_id=user.id, websocket=websocket)

            chat = await chat_storage.get_chat(chat_id)
            logger.debug("Processing the chat %s", chat)

            await _load_chat_messages(user.id, chat)

            try:
                while True:
                    text = await websocket.receive_text()
                    message = Message(chat_id=chat_id, user_id=user.id, text=text)
                    await chat_storage.add_message(chat_id=chat_id, message=message)
                    await web_socket_connection_manager.broadcast_to_users(
                        chat.user_ids, message=message
                    )

            except WebSocketDisconnect:
                web_socket_connection_manager.disconnect(
                    user_id=user.id, websocket=websocket
                )
                text = f"User left the chat"
                message = Message(chat_id=chat_id, user_id=user.id, text=text)
                await chat_storage.add_message(chat_id=chat_id, message=message)
                await web_socket_connection_manager.broadcast_to_users(
                    chat.user_ids, message=message
                )
