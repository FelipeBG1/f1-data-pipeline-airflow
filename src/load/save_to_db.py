import pandas as pd
from src.utils.db_connection import get_engine

def save_to_db(df, table):
    engine = get_engine()
    df.to_sql(table, con=engine, if_exists='replace', index=False)
    engine.dispose()

