from pathlib import Path
from typing import Any

import yaml

CONFIG_PATHS = [
    Path("config.yaml"),
    Path.home() / ".config" / "tradpas" / "config.yaml",
    Path("/etc/tradpas/config.yaml"),
]


class Config:
    def __init__(self, path: Path | None = None) -> None:
        self._data: dict[str, Any] = {}
        self._load(path)

    def _load(self, path: Path | None = None) -> None:
        if path is None:
            for p in CONFIG_PATHS:
                if p.exists():
                    path = p
                    break
            if path is None:
                path = CONFIG_PATHS[0]

        with open(path) as f:
            self._data = yaml.safe_load(f) or {}

    @property
    def telegram_api_id(self) -> int:
        return self._data.get("telegram", {}).get("api_id", 0)

    @property
    def telegram_api_hash(self) -> str:
        return self._data.get("telegram", {}).get("api_hash", "")

    @property
    def telegram_phone(self) -> str:
        return self._data.get("telegram", {}).get("phone", "")

    @property
    def telegram_bot_token(self) -> str:
        return self._data.get("telegram", {}).get("bot_token", "")

    @property
    def watch_channels(self) -> list[str]:
        return self._data.get("telegram", {}).get("watch_channels", [])

    @property
    def ollama_model(self) -> str:
        return self._data.get("analysis", {}).get("ollama", {}).get("model", "qwen2.5-coder")

    @property
    def ollama_host(self) -> str:
        return self._data.get("analysis", {}).get("ollama", {}).get("host", "http://localhost:11434")

    @property
    def confidence_threshold(self) -> float:
        return float(self._data.get("analysis", {}).get("confidence_threshold", 60))

    @property
    def cache_ttl(self) -> int:
        return int(self._data.get("analysis", {}).get("cache_ttl", 300))

    @property
    def notify_target(self) -> str:
        return self._data.get("notify", {}).get("target", "")
