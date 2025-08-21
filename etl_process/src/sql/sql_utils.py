import pandas as pd
from pathlib import Path
from etl_process.src.utils.db_engine import db_engine

def run_sql_query(query_path: str) -> pd.DataFrame:
    engine = db_engine(db="TARGET")
    query = Path(query_path).read_text()
    df = pd.read_sql(query, engine)
    return df
