import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

def get_engine(db='TARGET'):
    """Create a SQLAlchemy engine for the given db (SOURCE or TARGET)."""
    user = os.getenv(f"{db}_DB_USER")
    password = os.getenv(f"{db}_DB_PASSWORD")
    host = os.getenv(f"{db}_DB_HOST")
    port = os.getenv(f"{db}_DB_PORT")
    database = os.getenv(f"{db}_DB_NAME")

    engine = create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{database}")
    return engine


def load_data():
    """Load cleaned CSV into target database."""
    # 1. Read cleaned CSV
    df = pd.read_csv("data/processed/ae_data_cleaned.csv")

    # 2. Connect to target database
    engine = get_engine('TARGET')

    # 3. Load DataFrame into SQL
    df.to_sql(
        name="ae_attendances",   # table name in SQL
        con=engine,
        if_exists="replace",     # "replace" drops & recreates, use "append" to add rows
        index=False
    )
    print("✅ Data successfully loaded into target database!")


if __name__ == "__main__":
    load_data()
