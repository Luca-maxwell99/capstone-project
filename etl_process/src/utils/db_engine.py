import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# load environment variables
load_dotenv()

def db_engine(db='SOURCE'):
    
    '''engine = create_engine('postgresql://USER:PASSWORD@HOST:PORT/DATABASE')'''
    
    user = os.getenv(f'{db}_DB_USER')
    password = os.getenv(f'{db}_DB_PASSWORD')
    host = os.getenv(f'{db}_DB_HOST')
    port = os.getenv(f'{db}_DB_PORT')
    database = os.getenv(f'{db}_DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    return engine
