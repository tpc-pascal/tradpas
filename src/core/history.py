from src.database import db


def get_recent(limit: int = 20) -> list[dict]:
    return db.get_recent(limit)


def get_stats() -> dict:
    return db.get_stats()


def mark_entered(order_id: int) -> None:
    db.update_status(order_id, "entered")


def mark_skipped(order_id: int) -> None:
    db.update_status(order_id, "skipped")
