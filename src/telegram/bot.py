from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from src.core.order import Order
from src.database import db
from src.logger import logger


class SignalBot:
    def __init__(self, token: str, target: str) -> None:
        self.token = token
        self.target = target
        self.app: Application | None = None

    async def _start_cmd(self, update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "tradpas đang chạy.\n"
            "Khi có tín hiệu mới, tôi sẽ gửi vào đây."
        )

    async def _button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        data = query.data
        if data == "enter":
            await query.edit_message_text(
                text=query.message.text + "\n\n✅ Đã đánh dấu Vào lệnh."
            )
        elif data == "skip":
            await query.edit_message_text(
                text=query.message.text + "\n\n❌ Đã bỏ qua."
            )
        else:
            await query.edit_message_text(
                text=query.message.text + "\n\n⏭️ Đã bỏ qua."
            )

    def build(self) -> Application:
        self.app = Application.builder().token(self.token).build()

        self.app.add_handler(CommandHandler("start", self._start_cmd))
        self.app.add_handler(CallbackQueryHandler(self._button_callback))

        return self.app

    async def send_order(self, order: Order, order_id: int) -> None:
        if not self.app:
            return

        icon = "🟢" if order.direction.upper() == "LONG" else "🔴"

        text = (
            f"{icon} {order.symbol} {order.direction}\n"
            f"Entry: {order.entry:,.2f}\n"
            f"TP:   {order.tp:,.2f} ({order.tp_pct:+.2f}%)\n"
            f"SL:   {order.sl:,.2f} ({order.sl_pct:+.2f}%)\n"
            f"R:R:  {order.risk_reward_ratio}\n"
            f"Confidence: {order.confidence:.0f}%\n"
        )

        if order.reason:
            text += f"\n{order.reason}"

        keyboard = [
            [
                InlineKeyboardButton("✅ Vào lệnh", callback_data="enter"),
                InlineKeyboardButton("❌ Bỏ qua", callback_data="skip"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await self.app.bot.send_message(
                chat_id=self.target,
                text=text,
                reply_markup=reply_markup,
            )
            logger.info("Sent order #%d to %s", order_id, self.target)
        except Exception as e:
            logger.error("Failed to send order #%d: %s", order_id, e)
