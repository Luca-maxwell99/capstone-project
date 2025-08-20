import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd # type: ignore
from pathlib import Path

def read_input(limit: int | None = None):
    """Read cleaned CSV from processed data folder."""
    file_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "location_ae_combined.csv"


    if not file_path.exists():
        raise FileNotFoundError(f"No input found at {file_path}")

    df = pd.read_csv(file_path)

    if limit and len(df) > limit:
        df = df.head(limit)

    return df
