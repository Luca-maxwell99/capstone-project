import pandas as pd
from pathlib import Path
from etl_process.src.utils.db_engine import db_engine


def load_operational_data() -> pd.DataFrame:
    """
    Load operational (A&E) data from the target database.

    This function:
    - Establishes a connection to the target database.
    - Reads a SQL query from the `seen_within_4hrs.sql` file.
    - Executes the query against the database.
    - Returns the results as a pandas DataFrame.

    Returns:
        pd.DataFrame: Query results containing operational A&E data.
    """
    # Create a connection to the target database
    engine = db_engine(db="TARGET")

    # Debugging: print the database URL (optional, can be commented out in production)
    # print(engine.url)

    # Load SQL query from external file (keeps logic modular)
    sql_path = Path("etl_process/src/sql/seen_within_4hrs.sql")
    query = sql_path.read_text()

    # Execute query and load results into a pandas DataFrame
    df = pd.read_sql(query, engine)
    return df


def load_geospatial_data() -> pd.DataFrame:
    """
    Load geospatial A&E data from the target database.

    This function:
    - Establishes a connection to the target database.
    - Reads a SQL query from the `geospatial.sql` file.
    - Executes the query against the database.
    - Converts the 'period' column to datetime if necessary.
    - Returns the results as a pandas DataFrame.

    Returns:
        pd.DataFrame: Query results containing geospatial A&E data.
    """
    # Create a connection to the target database
    engine = db_engine(db="TARGET")

    # Load SQL query from external file
    sql_path = Path("etl_process/src/sql/geospatial.sql")
    query = sql_path.read_text()

    # Execute query and load results into a pandas DataFrame
    df = pd.read_sql(query, engine)

    # Ensure 'period' column is parsed as datetime for correct time-series handling
    if not pd.api.types.is_datetime64_any_dtype(df["period"]):
        df["period"] = pd.to_datetime(df["period"])

    return df
