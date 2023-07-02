import abc

from bot.settings import BotSettings


class IBot(abc.ABC):
    @abc.abstractmethod
    def on_message(self, ws, message):
        pass

    @abc.abstractmethod
    def on_error(self, ws, error):
        pass

    @abc.abstractmethod
    def on_close(self, ws, close_status_code, close_msg):
        pass

    @abc.abstractmethod
    def on_open(self, ws):
        pass
