import sqlite3
from datetime import datetime
from pathlib import Path

from src.logger import logger

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "history.db"


class Database:
    def __init__(self, path: Path = DB_PATH) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry REAL NOT NULL,
                tp REAL NOT NULL,
                sl REAL NOT NULL,
                order_type TEXT DEFAULT 'MARKET',
                confidence REAL DEFAULT 0,
                reason TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                raw_message TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    def save_order(
        self,
        symbol: str,
        direction: str,
        entry: float,
        tp: float,
        sl: float,
        order_type: str = "MARKET",
        confidence: float = 0.0,
        reason: str = "",
        raw_message: str = "",
    ) -> int:
        conn = self._get_conn()
        cursor = conn.execute(
            """INSERT INTO orders (symbol, direction, entry, tp, sl, order_type, confidence, reason, raw_message)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (symbol, direction, entry, tp, sl, order_type, confidence, reason, raw_message),
        )
        conn.commit()
        order_id = cursor.lastrowid
        logger.info("Saved order #%d: %s %s @ %.2f", order_id, symbol, direction, entry)
        return order_id

    def update_status(self, order_id: int, status: str) -> None:
        conn = self._get_conn()
        conn.execute(
            "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, order_id),
        )
        conn.commit()
        logger.info("Order #%d status -> %s", order_id, status)

    def get_recent(self, limit: int = 20) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM orders ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]

    def get_stats(self) -> dict:
        conn = self._get_conn()
        total = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        entered = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'entered'").fetchone()[0]
        skipped = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'skipped'").fetchone()[0]
        return {"total": total, "entered": entered, "skipped": skipped}

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None


db = Database()
