import os
from dotenv import load_dotenv
import pg8000
from pg8000.native import Connection

load_dotenv()

def db_conn(db='SOURCE'):
    '''
    parameters:
    
        db (str): 'SOURCE' or 'TARGET' - default is 'SOURCE'
    
    returns:
    
        database connection object
    
    '''
    conn = Connection(
        database=os.getenv(f'{db}_DB_NAME'),
        user=os.getenv(f'{db}_DB_USER'),
        password=os.getenv(f'{db}_DB_PASSWORD'),
        host=os.getenv(f'{db}_DB_HOST'),
        port=os.getenv(f'{db}_DB_PORT')
    )
    
    return conn