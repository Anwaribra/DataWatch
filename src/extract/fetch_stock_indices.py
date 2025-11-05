import pandas as pd
import logging
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import yfinance as yf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def get_db_connection_string():
    load_dotenv()
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'eis_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD')
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def fetch_stock_index(ticker, name):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max")
    df = hist.reset_index()[['Date', 'Close']]
    df.columns = ['date', 'index_value']
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['index_name'] = name
    return df

def fetch_all_indices():
    dfs = []
    indices = {'^GSPC': 'SP500', '^DJI': 'DOW'}
    for ticker, name in indices.items():
        df = fetch_stock_index(ticker, name)
        dfs.append(df)
        time.sleep(1)
    result = pd.concat(dfs)
    result_pivot = result.pivot_table(index='date', columns='index_name', values='index_value', aggfunc='last').reset_index()
    result_pivot.columns = [col.lower() if col != 'date' else col for col in result_pivot.columns]
    return result_pivot

def save_data(df):
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/stock_indices.csv', index=False)
    from sqlalchemy import create_engine
    engine = create_engine(get_db_connection_string())
    with engine.begin() as conn:
        df.to_sql('stock_indices', conn, if_exists='replace', index=False)
    logger.info("Data saved to PostgreSQL")

def main():
    df = fetch_all_indices()
    save_data(df)
    logger.info(f"Success: {len(df)} records")

if __name__ == "__main__":
    main()
