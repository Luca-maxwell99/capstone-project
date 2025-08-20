# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv(dotenv_path="../etl-process/.env")


DB_NAME = os.getenv("TARGET_DB_NAME")
DB_SCHEMA = os.getenv("TARGET_DB_SCHEMA")  # optional for schema-specific queries
DB_USER = os.getenv("TARGET_DB_USER")
DB_PASSWORD = os.getenv("TARGET_DB_PASSWORD")
DB_HOST = os.getenv("TARGET_DB_HOST")
DB_PORT = os.getenv("TARGET_DB_PORT")
DB_TABLE = os.getenv("TARGET_DB_TABLE")

# Create database connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Function to load data with caching
@st.cache_data
def load_data(table_name):
    query = f'SELECT * FROM {DB_SCHEMA}.{table_name} LIMIT 500'
    df = pd.read_sql(query, engine)
    return df

# Streamlit app
st.title("Database Table Viewer")
st.write(f"Showing data from table `{DB_SCHEMA}.{DB_TABLE}`")

data = load_data(DB_TABLE)
st.dataframe(data)



