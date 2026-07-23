import asyncio
from typing import Callable

from telethon import TelegramClient, events

from src.logger import logger
from src.config import Config

OnMessage = Callable[[str], None]


class SignalListener:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.client: TelegramClient | None = None
        self._running = False
        self._on_message: OnMessage | None = None

    def on_message(self, callback: OnMessage) -> None:
        self._on_message = callback

    async def start(self) -> None:
        self.client = TelegramClient(
            "tradpas_session",
            self.config.telegram_api_id,
            self.config.telegram_api_hash,
        )

        await self.client.start(phone=self.config.telegram_phone)
        logger.info("Logged in as %s", await self.client.get_me())

        @self.client.on(events.NewMessage(chats=self.config.watch_channels))
        async def handler(event: events.NewMessage) -> None:
            msg = event.message.text
            if not msg:
                return
            logger.info("Received message from %s", event.chat_id)
            if self._on_message:
                self._on_message(msg)

        self._running = True
        logger.info("Listening to channels: %s", self.config.watch_channels)
        await self.client.run_until_disconnected()

    async def stop(self) -> None:
        self._running = False
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected")
