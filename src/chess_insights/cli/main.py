from __future__ import annotations

import argparse

from chess_insights.data.ingest import load_games_from_pgn
from chess_insights.data.transform import games_to_dataframe
from chess_insights.core.analytics import compute_player_stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chess insights pipeline")
    parser.add_argument(
        "--pgn-path",
        type=str,
        required=True,
        help="Path to a PGN file with chess games.",
    )
    parser.add_argument(
        "--player",
        type=str,
        required=True,
        help="Player name to compute statistics for.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    games = load_games_from_pgn(args.pgn_path)
    df = games_to_dataframe(games)
    stats = compute_player_stats(df, args.player)

    print("=== Chess Insights ===")
    print(f"Player:       {stats['player']}")
    print(f"Total games:  {stats['total_games']}")
    print(f"Wins:         {stats['wins']}")
    print(f"Losses:       {stats['losses']}")
    print(f"Draws:        {stats['draws']}")
    print(f"Avg. moves:   {stats['avg_moves']:.2f}")


if __name__ == "__main__":
    main()
