from __future__ import annotations
from typing import Iterable

import pandas as pd
import chess.pgn


def games_to_dataframe(games: Iterable[chess.pgn.Game]) -> pd.DataFrame:
    """
    Convert an iterable of chess.pgn.Game objects into a Pandas DataFrame.

    Columns:
    - white: White player name
    - black: Black player name
    - result: Game result in PGN format (e.g. "1-0", "0-1", "1/2-1/2")
    - moves: Number of moves in the main line
    """
    records: list[dict[str, object]] = []

    for game in games:
        headers = game.headers
        result = headers.get("Result", "*")
        moves_count = len(list(game.mainline_moves()))

        records.append(
            {
                "white": headers.get("White", ""),
                "black": headers.get("Black", ""),
                "result": result,
                "moves": moves_count,
            }
        )

    return pd.DataFrame.from_records(records)
