from datetime import timedelta

from pydantic import BaseSettings


class BotSettings(BaseSettings):
    base_url: str = 'ws://127.0.0.1:8000/chat/ws/'
    chat_id: int
    token: str
    id: int

    request_duration = timedelta(seconds=3)

    @property
    def url(self):
        return self.base_url + str(self.chat_id)

    class Config:
        env_prefix="BOT_"
