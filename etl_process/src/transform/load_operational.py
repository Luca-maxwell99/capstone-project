import pandas as pd
from pathlib import Path
from etl_process.src.utils.db_engine import db_engine

def load_operational_data():
    engine = db_engine(db="TARGET")
    print(engine.url)  # Optional: helpful for debugging

    # Load SQL query from file
    sql_path = Path("etl_process/src/sql/seen_within_4hrs.sql")
    query = sql_path.read_text()

    # Execute query and return DataFrame
    df = pd.read_sql(query, engine)
    return df
