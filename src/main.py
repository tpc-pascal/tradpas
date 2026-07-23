import argparse
import asyncio
import signal
import sys

from src.config import Config
from src.logger import logger
from src.telegram.listener import SignalListener
from src.telegram.parser import parse_message
from src.telegram.bot import SignalBot
from src.core.processor import Processor


class App:
    def __init__(self, config_path: str | None = None) -> None:
        self.config = Config()
        self.listener = SignalListener(self.config)
        self.bot = SignalBot(
            token=self.config.telegram_bot_token,
            target=self.config.notify_target,
        )
        self.processor = Processor(self.config, self.bot)
        self._running = False

    async def run(self) -> None:
        bot_app = self.bot.build()
        await bot_app.initialize()
        await bot_app.start()

        self.listener.on_message(self._handle_message)
        await self.listener.start()

    async def shutdown(self) -> None:
        logger.info("Shutting down...")
        self._running = False
        await self.listener.stop()
        if self.bot.app:
            await self.bot.app.stop()

    def _handle_message(self, raw: str) -> None:
        order = parse_message(raw)
        if order is None:
            return
        asyncio.create_task(self.processor.process(order))

    def run_sync(self) -> None:
        self._running = True

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))
            except NotImplementedError:
                pass

        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            loop.run_until_complete(self.shutdown())
        finally:
            loop.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="tradpas - Telegram trading bot")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(__import__("logging").DEBUG)

    app = App(config_path=args.config)
    app.run_sync()


if __name__ == "__main__":
    sys.exit(main())
