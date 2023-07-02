import websocket
import rel

from bot.gptbot import GPTBot
from bot.settings import BotSettings
from bot.triton_client import TritonClient, TritonClientSettings

if __name__ == "__main__":
    bot_settings = BotSettings()
    triton_client_settings = TritonClientSettings()
    triton_client = TritonClient(triton_client_settings=triton_client_settings)
    bot = GPTBot(bot_settings=bot_settings, triton_client=triton_client)

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        bot_settings.url,
        header={"Cookie": f"session={bot_settings.token}"},
        on_open=bot.on_open,
        on_message=bot.on_message,
        on_error=bot.on_error,
        on_close=bot.on_close,
    )

    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()
