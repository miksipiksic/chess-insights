from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from metaflow import FlowSpec, step, Parameter


class ChessInsightsFlow(FlowSpec):
    """
    Metaflow pipeline for AI Chess Insights:
    - Load and parse PGN games
    - Extract features
    - Train an ML model
    - Evaluate performance
    """

    # --------- PARAMETERS ---------
    raw_pgn_dir = Parameter(
        "raw_pgn_dir",
        default="src/data",
        help="Directory containing raw PGN files.",
    )

    processed_dir = Parameter(
        "processed_dir",
        default="src/data/processed",
        help="Directory to store processed CSV and feature files.",
    )

    model_output_dir = Parameter(
        "model_output_dir",
        default="src/models",
        help="Directory to save trained models and metrics.",
    )

    test_size = Parameter(
        "test_size",
        default=0.2,
        help="Proportion of data used for testing (0–1).",
    )

    random_state = Parameter(
        "random_state",
        default=42,
        help="Random seed for reproducibility.",
    )

    # --------- PIPELINE STEPS ---------

    @step
    def start(self):
        """
        Initial setup – check paths, create folders, basic info.
        """
        print("🔹 Starting ChessInsightsFlow...")
         # Create Path versions of parameters WITHOUT overwriting them
        self.raw_pgn_path = Path(self.raw_pgn_dir)
        self.processed_path = Path(self.processed_dir)
        self.model_output_path = Path(self.model_output_dir)

        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.model_output_path.mkdir(parents=True, exist_ok=True)

        print(f"PGN directory: {self.raw_pgn_path}")
        print(f"Processed directory: {self.processed_path}")
        print(f"Model output directory: {self.model_output_path}")

        self.next(self.load_games)

    @step
    def load_games(self):
        """
        Load PGN games and convert them into a DataFrame.
        Replace the placeholder logic with your real PGN parser.
        """
        print("🔹 Loading PGN games...")

        games: List[Dict[str, Any]] = []

        for pgn_file in self.raw_pgn_path.glob("*.pgn"):
            print(f"  → reading {pgn_file.name}")
            # TODO: Replace with your own parser
            games.append(
                {
                    "game_id": pgn_file.stem,
                    "white": "PlayerA",
                    "black": "PlayerB",
                    "result": "1-0",
                    "moves": "e4 e5 Nf3 Nc6",
                }
            )

        self.games_df = pd.DataFrame(games)
        print(f"🔹 Loaded {len(self.games_df)} games")

        games_csv = self.processed_path / "games_raw.csv"
        self.games_df.to_csv(games_csv, index=False)
        print(f"✅ Saved raw data to {games_csv}")

        self.next(self.extract_features)

    @step
    def extract_features(self):
        """
        Convert raw game data into a feature set for ML.
        """
        print("🔹 Extracting features...")

        df = self.games_df.copy()

        # TODO: Add your feature extraction logic here
        df["num_moves"] = df["moves"].apply(lambda s: len(str(s).split()))
        df["is_white_win"] = (df["result"] == "1-0").astype(int)

        # Feature matrix (X) and target (y)
        feature_cols = ["num_moves"]
        target_col = "is_white_win"

        self.X = df[feature_cols]
        self.y = df[target_col]

        from sklearn.model_selection import train_test_split

        n_samples = len(self.X)

        if n_samples < 2:
            # Not enough data to make a proper train/test split
            print(f"⚠ Not enough samples for a train/test split (n={n_samples}).")
            print("⚠ Using all data for both training and testing – metrics will NOT be reliable.")

            self.X_train = self.X
            self.y_train = self.y
            self.X_test = self.X
            self.y_test = self.y
        else:
            (
                self.X_train,
                self.X_test,
                self.y_train,
                self.y_test,
            ) = train_test_split(
                self.X,
                self.y,
                test_size=float(self.test_size),
                random_state=int(self.random_state),
                stratify=self.y if n_samples > 1 else None,
            )

            
        print(f"🔹 Train size: {len(self.X_train)}, test size: {len(self.X_test)}")

        self.next(self.train_model)

    @step
    def train_model(self):
        """
        Train a simple ML model (Random Forest by default).
        """
        print("🔹 Training model...")

        from sklearn.ensemble import RandomForestClassifier
        from joblib import dump

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            random_state=int(self.random_state),
            n_jobs=-1,
        )
        model.fit(self.X_train, self.y_train)
        self.model = model

        model_path = self.model_output_path / "rf_chess_model.joblib"
        dump(model, model_path)
        print(f"✅ Model saved to {model_path}")

        self.next(self.evaluate)

    @step
    def evaluate(self):
        """
        Evaluate the trained model and store metrics.
        """
        print("🔹 Evaluating model...")

        from sklearn.metrics import accuracy_score, classification_report
        import json

        y_pred = self.model.predict(self.X_test)
        acc = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred, output_dict=True)

        self.metrics: Dict[str, Any] = {
            "accuracy": float(acc),
            "report": report,
        }

        print(f"✅ Accuracy: {acc:.4f}")

        metrics_path = self.model_output_path / "metrics.json"
        with metrics_path.open("w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2)
        print(f"✅ Metrics saved to {metrics_path}")

        self.next(self.end)

    @step
    def end(self):
        """
        Final step – print summary.
        """
        print("🎉 ChessInsightsFlow completed successfully!")
        print("Final accuracy:", self.metrics.get("accuracy", None))


if __name__ == "__main__":
    ChessInsightsFlow()
