import time

import requests

from src.config import Config
from src.core.order import Order
from src.logger import logger
from src.analysis.market import format_market_data
from src.analysis.news import fetch_news

CACHE: dict[str, tuple[float, float, str]] = {}


def _cache_key(order: Order) -> str:
    return f"{order.symbol}:{order.direction}:{order.entry}:{order.tp}:{order.sl}"


class Analyzer:
    def __init__(self, config: Config) -> None:
        self.config = config

    async def analyze(self, order: Order) -> tuple[float, str]:
        key = _cache_key(order)
        now = time.time()

        cached = CACHE.get(key)
        if cached and now - cached[0] < self.config.cache_ttl:
            logger.info("Cache hit for %s", key)
            return cached[1], cached[2]

        confidence = 50.0
        reason = "Phân tích cơ bản (không có LLM)"

        try:
            market_data = format_market_data(order.symbol)
            news = fetch_news()

            prompt_path = self.config._data.get("prompt_path", "prompts/analyze.txt")
            try:
                with open(prompt_path) as f:
                    prompt_template = f.read()
            except FileNotFoundError:
                prompt_template = (
                    "Analyze this {direction} order on {symbol}: "
                    "entry={entry}, tp={tp}, sl={sl}. "
                    "Market data:\n{market_data}\nNews:\n{news}\n"
                    "Return confidence 0-100 and reason."
                )

            prompt = prompt_template.format(
                symbol=order.symbol,
                direction=order.direction,
                entry=order.entry,
                tp=order.tp,
                sl=order.sl,
                market_data=market_data,
                news=news,
            )

            response = requests.post(
                f"{self.config.ollama_host}/api/generate",
                json={
                    "model": self.config.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )

            if response.status_code == 200:
                result = response.json().get("response", "")
                confidence, reason = self._parse_result(result, order)
            else:
                logger.error("Ollama error: %s", response.text)

        except Exception as e:
            logger.error("Analysis failed: %s", e)

        CACHE[key] = (now, confidence, reason)
        return confidence, reason

    def _parse_result(self, result: str, order: Order) -> tuple[float, str]:
        lines = result.strip().split("\n")
        confidence = 50.0
        reason = ""

        for line in lines:
            line = line.strip()
            if line.upper().startswith("CONFIDENCE:"):
                try:
                    num_str = line.split(":", 1)[1].strip()
                    confidence = float(num_str.replace("%", ""))
                    confidence = max(0.0, min(100.0, confidence))
                except ValueError:
                    pass
            elif line.upper().startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()

        if not reason:
            reason = f"Tín hiệu {order.direction} {order.symbol} với R:R={order.risk_reward_ratio}"

        return confidence, reason
