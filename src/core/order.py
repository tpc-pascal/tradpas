from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Order:
    symbol: str
    direction: str
    entry: float
    tp: float
    sl: float
    order_type: str = "MARKET"
    confidence: float = 0.0
    reason: str = ""
    raw_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def risk_reward_ratio(self) -> float:
        if self.direction.upper() == "LONG":
            reward = self.tp - self.entry
            risk = self.entry - self.sl
        else:
            reward = self.entry - self.tp
            risk = self.sl - self.entry
        if risk <= 0:
            return 0.0
        return round(reward / risk, 2)

    @property
    def tp_pct(self) -> float:
        return round((self.tp - self.entry) / self.entry * 100, 2)

    @property
    def sl_pct(self) -> float:
        return round((self.sl - self.entry) / self.entry * 100, 2)
