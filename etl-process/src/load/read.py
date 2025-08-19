import pandas as pd # type: ignore
from pathlib import Path

def read_input(limit: int | None = None):
    """Read cleaned CSV from processed data folder."""
    file_path = Path("data/processed/ae_data_cleaned.csv")

    if not file_path.exists():
        raise FileNotFoundError(f"No input found at {file_path}")

    df = pd.read_csv(file_path)

    if limit and len(df) > limit:
        df = df.head(limit)

    return df
