from starlette.websockets import WebSocket


class WebSocketConnectionManager:
    def __init__(self):
        self.user_id_to_web_sockets_map: dict[int, list[WebSocket]] = {}

    def connect(self, user_id: int, websocket: WebSocket):
        user_websockets = self.user_id_to_web_sockets_map.get(user_id, [])
        user_websockets.append(websocket)
        self.user_id_to_web_sockets_map[user_id] = user_websockets

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.user_id_to_web_sockets_map[user_id].remove(websocket)

    async def broadcast_to_users(self, user_ids: list[int], message: str):
        for user_id in user_ids:
            for websocket in self.user_id_to_web_sockets_map.get(user_id, []):
                await websocket.send_text(message)
