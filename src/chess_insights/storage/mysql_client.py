from __future__ import annotations

from typing import Any
import os

import mysql.connector
from mysql.connector.connection import MySQLConnection
from dotenv import load_dotenv


_env_loaded = False


def _ensure_env_loaded() -> None:
    global _env_loaded
    if not _env_loaded:
        load_dotenv()
        _env_loaded = True


def get_mysql_connection() -> MySQLConnection:
    """
    Create and return a MySQL connection using environment variables.
    """
    _ensure_env_loaded()

    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER", "chess")
    password = os.getenv("MYSQL_PASSWORD", "chesspass")
    database = os.getenv("MYSQL_DB", "chess_insights")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )


def insert_game_stats(stats: dict[str, Any]) -> None:
    """
    Insert a single row of player statistics into the game_stats table.
    """
    conn = get_mysql_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO game_stats (player, total_games, wins, losses, draws, avg_moves)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            stats["player"],
            stats["total_games"],
            stats["wins"],
            stats["losses"],
            stats["draws"],
            stats["avg_moves"],
        ),
    )

    conn.commit()
    cursor.close()
    conn.close()
