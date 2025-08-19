import os
from src.utils.db_engine import db_engine

# This file wraps my existing database engine 

def get_engine(db="TARGET"):
    """Return a SQLAlchemy engine for SOURCE or TARGET database."""
    return db_engine(db)

# And provides schema/table info 

def get_target():
    """Return schema and table name for target database."""
    schema = os.getenv("TARGET_DB_SCHEMA") or "public"
    table = os.getenv("TARGET_DB_TABLE") or "ae_attendances"
    return schema, table
