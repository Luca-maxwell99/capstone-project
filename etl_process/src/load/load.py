import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.load.db import get_engine, get_target
from src.load.read import read_input

def load_data(limit: int | None = None):
    """Load processed CSV into target database."""
    # 1. Read data
    df = read_input(limit)

    # 2. Get engine + target table info
    engine = get_engine("TARGET")
    schema, table = get_target()

    # 3. Load into SQL
    df.to_sql(
        name=table,
        con=engine,
        schema=schema,
        if_exists="replace",   # replace table, use "append" if you want to keep history
        index=False
    )

    print(f"Data successfully loaded into {schema}.{table}!")

if __name__ == "__main__":
    load_data()

