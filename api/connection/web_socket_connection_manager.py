import logging

from starlette.websockets import WebSocket

from api.storage.message import Message

logger = logging.getLogger(__name__)


class WebSocketConnectionManager:
    def __init__(self):
        self.user_id_to_web_sockets_map: dict[int, list[WebSocket]] = {}

    def connect(self, user_id: int, websocket: WebSocket):
        user_websockets = self.user_id_to_web_sockets_map.get(user_id, [])
        user_websockets.append(websocket)
        self.user_id_to_web_sockets_map[user_id] = user_websockets
        logger.debug("User %s connected, websockets: %s", user_id, user_websockets)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.user_id_to_web_sockets_map[user_id].remove(websocket)
        logger.debug(
            "User %s disconnected, websockets: %s",
            user_id,
            self.user_id_to_web_sockets_map[user_id],
        )

    async def broadcast_to_users(self, user_ids: list[int], message: Message):
        for user_id in user_ids:
            logger.debug("Try to send message to user %s", user_id)

            for websocket in self.user_id_to_web_sockets_map.get(user_id, []):
                logger.debug(
                    "Send message %s to user %s, into socket %s ",
                    message,
                    user_id,
                    websocket,
                )
                await websocket.send_text(str(message))
