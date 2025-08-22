# run_etl.py
import os
import sys
from pathlib import Path

# Add etl_process/ to Python path so top-level modules like config/ can be imported
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config.env_config import setup_env
from src.transform.transform_ae import transform_ae_data
from src.load.load import load_data

def main():
    setup_env(sys.argv)
    env = os.getenv('ENV', 'error')
    print(f"ETL pipeline starting in '{env}' environment...")

    try:
        # Transform step
        cleaned_df = transform_ae_data()
        print(f"Transformation complete. Rows: {len(cleaned_df)}")

        # Load step (reads from saved CSV)
        load_data()
        print("ETL pipeline completed successfully.")

    except Exception as e:
        print(f"ETL pipeline failed: {e}")

if __name__ == "__main__":
    main()
