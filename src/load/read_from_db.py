import pandas as pd
from src.utils.db_connection import get_engine

def read_from_db(table):

    engine = get_engine()
    try:     
        df = pd.read_sql(f"SELECT * FROM {table}", con=engine)
        return df
    finally:
        engine.dispose()

def read_from_db_by_query(query, env_path=".env"):
    engine = get_engine(env_path)
    try:     
        df = pd.read_sql(query, con=engine)
        return df
    finally:
        engine.dispose()