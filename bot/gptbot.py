import re
import time

from bot.bot_interface import IBot
from bot.settings import BotSettings
from bot.triton_client import TritonClient


class GPTBot(IBot):
    def __init__(self, bot_settings: BotSettings, triton_client: TritonClient):
        self._bot_settings = bot_settings
        self._time_of_last_message = None
        self._is_request_being_processed = False
        self._triton_client = triton_client

    def on_message(self, ws, message):
        print(message)
        reg = re.compile(r'\((?P<user_id>\d+)\): (?P<message>.+)')
        match = reg.match(message)
        if not match:
            print('Did not match regex')
            return
        groups = match.groupdict()
        user_id = int(groups['user_id'])
        if user_id == self._bot_settings.id:
            return
        message = groups['message']

        if self._should_process_message():
            ws.send(self._auto_complete(text=message))
        else:
            ws.send('Wait a little!')

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        self._reset()

    def on_open(self, ws):
        self._reset()

    def _reset(self):
        self._time_of_last_message = None
        self._is_request_being_processed = False

    def _should_process_message(self) -> bool:
        if self._is_request_being_processed:
            return False

        current_time = time.perf_counter()
        if self._time_of_last_message is not None:
            diff = current_time - self._time_of_last_message
            self._time_of_last_message = current_time
            return diff > self._bot_settings.request_duration.total_seconds()

        self._time_of_last_message = current_time

    def _auto_complete(self, text: str) -> str:
        try:
            self._is_request_being_processed = True
            return self._triton_client.auto_complete(text)
        finally:
            self._is_request_being_processed = False
