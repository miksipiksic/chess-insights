from __future__ import annotations
from typing import Iterable

import chess.pgn


def load_games_from_pgn(path: str) -> Iterable[chess.pgn.Game]:
    """
    Load chess games from a PGN file.

    :param path: Filesystem path to a .pgn file
    :return: Iterable of chess.pgn.Game objects
    """
    with open(path, "r", encoding="utf-8") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            yield game
