import feedparser
from typing import Final

FEEDS: Final[list[str]] = [
    "https://coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]

MAX_ITEMS: Final[int] = 5


def fetch_news() -> str:
    headlines: list[str] = []

    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_ITEMS]:
                title = entry.get("title", "").strip()
                if not title:
                    continue
                link = entry.get("link", "")
                headlines.append(f"- {title}")
                if len(headlines) >= MAX_ITEMS:
                    break
            if len(headlines) >= MAX_ITEMS:
                break
        except Exception:
            continue

    if not headlines:
        return "No news available"

    return "\n".join(headlines[:MAX_ITEMS])
