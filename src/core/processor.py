from src.config import Config
from src.core.order import Order
from src.database import db
from src.logger import logger
from src.telegram.bot import SignalBot
from src.analysis.analyzer import Analyzer


class Processor:
    def __init__(self, config: Config, bot: SignalBot) -> None:
        self.config = config
        self.bot = bot
        self.analyzer = Analyzer(config)

    async def process(self, order: Order) -> None:
        confidence, reason = await self.analyzer.analyze(order)

        order.confidence = confidence
        order.reason = reason

        order_id = db.save_order(
            symbol=order.symbol,
            direction=order.direction,
            entry=order.entry,
            tp=order.tp,
            sl=order.sl,
            order_type=order.order_type,
            confidence=confidence,
            reason=reason,
            raw_message=order.raw_message,
        )

        if confidence >= self.config.confidence_threshold:
            logger.info(
                "Order #%d: confidence %.0f%% >= %d%%, sending notification",
                order_id, confidence, self.config.confidence_threshold,
            )
            await self.bot.send_order(order, order_id)
        else:
            logger.info(
                "Order #%d: confidence %.0f%% < %d%%, skipped",
                order_id, confidence, self.config.confidence_threshold,
            )
