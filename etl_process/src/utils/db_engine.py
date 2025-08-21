import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()


def db_engine(db: str = 'SOURCE'):
    """
    Create a SQLAlchemy engine for connecting to a PostgreSQL database.

    The database credentials are read from environment variables, following the pattern:
        {DB}_DB_USER, {DB}_DB_PASSWORD, {DB}_DB_HOST, {DB}_DB_PORT, {DB}_DB_NAME
    where {DB} is either "SOURCE" or "TARGET" by default.

    Args:
        db (str): The database to connect to, either "SOURCE" or "TARGET". Default is "SOURCE".

    Returns:
        sqlalchemy.engine.base.Engine: SQLAlchemy engine object for database connection.

    Example:
        engine = db_engine(db="TARGET")
    """
    
    # Fetch database credentials from environment variables
    user = os.getenv(f'{db}_DB_USER')
    password = os.getenv(f'{db}_DB_PASSWORD')
    host = os.getenv(f'{db}_DB_HOST')
    port = os.getenv(f'{db}_DB_PORT')
    database = os.getenv(f'{db}_DB_NAME')
    
    # Construct the SQLAlchemy engine URL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    return engine
