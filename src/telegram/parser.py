import re
from typing import Final

from src.core.order import Order
from src.logger import logger

PATTERNS: Final[list[tuple[str, str]]] = [
    (r"((?:BTC|ETH|SOL|DOGE|BNB|XRP|ADA|AVAX|DOT|LINK|UNI|PEPE|WIF)\s*(?:USDT|USD))", "symbol"),
    (r"(LONG|SHORT|BUY|SELL)", "direction"),
    (r"(?:Entry|ENTRY|Vào|entry)\s*[:\s]*([\d.,]+)", "entry"),
    (r"(?:TP|TAKE\s*PROFIT|Take\s*Profit|tp)\s*[:\s]*([\d.,]+)", "tp"),
    (r"(?:SL|STOP\s*LOSS|Stop\s*Loss|sl)\s*[:\s]*([\d.,]+)", "sl"),
    (r"(?:MARKET|Limit|LIMIT)", "order_type"),
]


def _clean_number(text: str) -> float:
    return float(text.replace(",", "").replace(".", "."))


def parse_message(raw: str) -> Order | None:
    if not raw:
        return None

    data: dict[str, str | float] = {}
    text = raw.strip().upper()

    for pattern, key in PATTERNS:
        match = re.search(pattern, text)
        if match:
            if key in ("symbol", "direction", "order_type"):
                val = match.group(0).capitalize() if len(match.groups()) == 0 else match.group(1).upper()
                data[key] = val
            else:
                try:
                    data[key] = _clean_number(match.group(1))
                except (ValueError, IndexError):
                    continue

    required = {"symbol", "direction", "entry", "tp", "sl"}
    missing = required - set(data.keys())
    if missing:
        logger.warning("Missing fields %s in message: %.80s", missing, raw)
        return None

    direction = str(data.get("direction", "LONG"))
    if direction in ("BUY",):
        direction = "LONG"
    elif direction in ("SELL",):
        direction = "SHORT"

    order_type = str(data.get("order_type", "MARKET")).upper()
    if order_type not in ("MARKET", "LIMIT"):
        order_type = "MARKET"

    return Order(
        symbol=str(data["symbol"]),
        direction=direction,
        entry=float(data["entry"]),
        tp=float(data["tp"]),
        sl=float(data["sl"]),
        order_type=order_type,
        raw_message=raw,
    )
