from __future__ import annotations

import argparse

from dotenv import load_dotenv

from chess_insights.data.ingest import load_games_from_pgn
from chess_insights.data.transform import games_to_dataframe
from chess_insights.core.analytics import compute_player_stats
from chess_insights.storage.redis_client import get_cached_stats, set_cached_stats
from chess_insights.storage.mysql_client import insert_game_stats



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
    parser.add_argument(
        "--use-redis-cache",
        action="store_true",
        help="Read/write player statistics from Redis cache.",
    )

    parser.add_argument(
        "--store-in-mysql",
        action="store_true",
        help="Store computed player statistics in MySQL.",
    )

    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    # 1) Try Redis cache first (if enabled)
    if args.use_redis_cache:
        cached = get_cached_stats(args.player)
        if cached is not None:
            print("=== Chess Insights (from Redis cache) ===")
            print(f"Player:       {cached['player']}")
            print(f"Total games:  {cached['total_games']}")
            print(f"Wins:         {cached['wins']}")
            print(f"Losses:       {cached['losses']}")
            print(f"Draws:        {cached['draws']}")
            print(f"Avg. moves:   {cached['avg_moves']:.2f}")
            return

    # 2) Load games and compute stats
    games = load_games_from_pgn(args.pgn_path)
    df = games_to_dataframe(games)
    stats = compute_player_stats(df, args.player)

    # 3) Store in Redis (if enabled)
    if args.use_redis_cache:
        set_cached_stats(args.player, stats)
    
    if args.store_in_mysql:
        insert_game_stats(stats)

    print("=== Chess Insights ===")
    print(f"Player:       {stats['player']}")
    print(f"Total games:  {stats['total_games']}")
    print(f"Wins:         {stats['wins']}")
    print(f"Losses:       {stats['losses']}")
    print(f"Draws:        {stats['draws']}")
    print(f"Avg. moves:   {stats['avg_moves']:.2f}")


if __name__ == "__main__":
    main()
