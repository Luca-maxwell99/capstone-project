import pandas as pd
from pathlib import Path
from etl_process.src.utils.db_engine import db_engine
from etl_process.src.sql.sql_utils import run_sql_query  # Fixed import

def load_latest_summary() -> pd.DataFrame:
    """
    Load the latest summary data for the homepage from the target database.

    Steps:
    - Connects to the target database using `db_engine`.
    - Reads the SQL query from `latest_home.sql`.
    - Executes the query and returns the results as a pandas DataFrame.

    Returns:
        pd.DataFrame: Latest summary data for use on the homepage.
    """
    # Establish connection to the target database
    engine = db_engine(db="TARGET")

    # Load SQL query from file
    sql_path = Path("etl_process/src/sql/latest_home.sql")
    query = sql_path.read_text()

    # Execute query and return results as DataFrame
    df = pd.read_sql(query, engine)
    return df


def load_national_trends() -> pd.DataFrame:
    """
    Load national trend data for homepage visualisations.

    Currently, this function simply reuses the latest summary query.
    Can be modified later if national trends require a separate query.

    Returns:
        pd.DataFrame: National trend summary data.
    """
    return load_latest_summary()


def load_trust_12hr_summary() -> pd.DataFrame:
    """
    Load 12-hour wait summary data by trust.

    Steps:
    - Uses the utility function `run_sql_query` to execute the query in
      `trust_12hr_summary.sql`.
    - Returns the results as a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing 12-hour wait summary by trust.
    """
    # Path to SQL query file
    query_path = "etl_process/src/sql/trust_12hr_summary.sql"

    # Execute SQL and return results
    df = run_sql_query(query_path)
    return df
