from chess_insights.core.analytics import compute_player_stats
import pandas as pd


def test_compute_player_stats_basic():
    # Prepare sample DataFrame (same data as sample_games.pgn)
    df = pd.DataFrame([
        {"white": "Milena", "black": "Opponent1", "result": "1-0", "moves": 20},
        {"white": "Opponent2", "black": "Milena", "result": "0-1", "moves": 18},
        {"white": "Milena", "black": "Opponent3", "result": "1/2-1/2", "moves": 22},
    ])

    stats = compute_player_stats(df, "Milena")

    assert stats["player"] == "Milena"
    assert stats["total_games"] == 3
    assert stats["wins"] == 2
    assert stats["losses"] == 0
    assert stats["draws"] == 1
    # average moves should be around 20.0
    assert abs(stats["avg_moves"] - 20.0) < 0.01
