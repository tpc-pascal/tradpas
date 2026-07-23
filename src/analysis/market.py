import ccxt
from typing import Final

EXCHANGE: Final[dict] = {
    "enableRateLimit": True,
    "options": {"defaultType": "spot"},
}

CACHE: dict[str, dict] = {}
CACHE_TTL: Final[int] = 60


def get_ticker(symbol: str) -> dict[str, float] | None:
    now = __import__("time").time()
    cached = CACHE.get(symbol)
    if cached and now - cached["time"] < CACHE_TTL:
        return cached["data"]

    try:
        exchange = ccxt.binance(EXCHANGE)
        ticker = exchange.fetch_ticker(symbol)
        data = {
            "price": ticker.get("last", 0) or 0,
            "high": ticker.get("high", 0) or 0,
            "low": ticker.get("low", 0) or 0,
            "volume": ticker.get("baseVolume", 0) or 0,
            "change": ticker.get("percentage", 0) or 0,
        }
        CACHE[symbol] = {"data": data, "time": now}
        return data
    except Exception:
        return None


def format_market_data(symbol: str) -> str:
    data = get_ticker(symbol)

    if data is None:
        return f"No market data available for {symbol}"

    change_str = f"{data['change']:+.2f}%"
    return (
        f"Symbol: {symbol}\n"
        f"Price: {data['price']:.2f}\n"
        f"24h High: {data['high']:.2f}\n"
        f"24h Low: {data['low']:.2f}\n"
        f"24h Volume: {data['volume']:.2f}\n"
        f"24h Change: {change_str}"
    )
