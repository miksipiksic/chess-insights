from __future__ import annotations
from typing import Any

import pandas as pd


def compute_player_stats(df: pd.DataFrame, player: str) -> dict[str, Any]:
    """
    Compute basic statistics for a given player.

    Stats:
    - total_games
    - wins
    - losses
    - draws
    - avg_moves
    """

    mask_white = df["white"] == player
    mask_black = df["black"] == player
    player_games = df[mask_white | mask_black].copy()

    total = len(player_games)
    if total == 0:
        return {
            "player": player,
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "avg_moves": 0.0,
        }

    def is_win(row: pd.Series) -> bool:
        if row["white"] == player and row["result"] == "1-0":
            return True
        if row["black"] == player and row["result"] == "0-1":
            return True
        return False

    def is_draw(row: pd.Series) -> bool:
        return row["result"] == "1/2-1/2"

    wins = int(player_games.apply(is_win, axis=1).sum())
    draws = int(player_games.apply(is_draw, axis=1).sum())
    losses = total - wins - draws
    avg_moves = float(player_games["moves"].mean())

    return {
        "player": player,
        "total_games": total,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "avg_moves": avg_moves,
    }
