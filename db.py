import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

DB_PATH = Path("modbot.sqlite3")

class Database:
    def __init__(self, path: Path = DB_PATH) -> None:
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    moderator_id INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL
                )
                """
            )

    # --- basic functions ---

    def add_warning(self, *, user_id: int, moderator_id: int, guild_id: int, reason: str) -> None:
        ts = int(time.time())
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO warnings (user_id, moderator_id, reason, timestamp, guild_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, moderator_id, reason, ts, guild_id),
            )

    def get_warnings_for_user(
        self, *, user_id: int, guild_id: int, limit: int = 10
    ) -> list[sqlite3.Row]:
        cur = self._conn.execute(
            """
            SELECT id, user_id, moderator_id, reason, timestamp, guild_id
            FROM warnings
            WHERE user_id = ? AND guild_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (user_id, guild_id, limit),
        )
        return list(cur.fetchall())

    def get_total_warnings(self, guild_id: int | None = None) -> int:
        if guild_id is None:
            cur = self._conn.execute("SELECT COUNT(*) AS c FROM warnings")
            row = cur.fetchone()
            return int(row["c"]) if row else 0

        cur = self._conn.execute(
            "SELECT COUNT(*) AS c FROM warnings WHERE guild_id = ?",
            (guild_id,),
        )
        row = cur.fetchone()
        return int(row["c"]) if row else 0

    def get_stats_for_guild(self, *, guild_id: int, top_n: int = 5) -> dict[str, Any]:
        total = self.get_total_warnings(guild_id=guild_id)

        cur_unique = self._conn.execute(
            "SELECT COUNT(DISTINCT user_id) AS c FROM warnings WHERE guild_id = ?",
            (guild_id,),
        )
        row_unique = cur_unique.fetchone()
        unique_users = int(row_unique["c"]) if row_unique else 0

        cur_top = self._conn.execute(
            """
            SELECT user_id, COUNT(*) AS warning_count
            FROM warnings
            WHERE guild_id = ?
            GROUP BY user_id
            ORDER BY warning_count DESC
            LIMIT ?
            """,
            (guild_id, top_n),
        )
        top_rows = list(cur_top.fetchall())

        return {
            "total_warnings": total,
            "unique_users": unique_users,
            "top_users": top_rows,
        }
        
    def get_warnings_per_moderator(self, *, guild_id: int) -> list[sqlite3.Row]:
        cur = self._conn.execute(
            """
            SELECT moderator_id, COUNT(*) AS count
            FROM warnings
            WHERE guild_id = ?
            GROUP BY moderator_id
            ORDER BY count DESC
            """,
            (guild_id,),
        )
        return list(cur.fetchall())

    def get_warnings_per_day(self, *, guild_id: int, days: int = 7) -> list[sqlite3.Row]:
        cur = self._conn.execute(
            """
            SELECT
                DATE(timestamp, 'unixepoch') AS day,
                COUNT(*) AS count
            FROM warnings
            WHERE guild_id = ?
              AND timestamp >= strftime('%s', 'now', ? || ' days')
            GROUP BY day
            ORDER BY day ASC
            """,
            (guild_id, f"-{days}"),
        )
        return list(cur.fetchall())


db = Database()