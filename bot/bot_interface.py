import abc

from bot.settings import BotSettings


class IBot(abc.ABC):
    @abc.abstractmethod
    def on_message(self, ws, message):
        print(message)
        ws.send("Hello, World")

    @abc.abstractmethod
    def on_error(self, ws, error):
        print(error)

    @abc.abstractmethod
    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    @abc.abstractmethod
    def on_open(self, ws):
        print("Opened connection")
