import pandas as pd
from pathlib import Path
from etl_process.src.utils.db_engine import db_engine
from etl_process.src.sql.sql_utils import run_sql_query  # ✅ fixed import

def load_latest_summary():
    engine = db_engine(db="TARGET")
    sql_path = Path("etl_process/src/sql/latest_home.sql")
    query = sql_path.read_text()
    df = pd.read_sql(query, engine)
    return df

def load_national_trends():
    return load_latest_summary()

def load_trust_12hr_summary():
    query_path = "etl_process/src/sql/trust_12hr_summary.sql"
    df = run_sql_query(query_path)
    return df
