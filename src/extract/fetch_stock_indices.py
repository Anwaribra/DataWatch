import requests
import pandas as pd
import logging
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

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
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return connection_string

def fetch_stock_index(ticker, name):
    if not YFINANCE_AVAILABLE:
        return None
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")
        if hist.empty:
            return None
        df = hist.reset_index()[['Date', 'Close']]
        df.columns = ['date', 'index_value']
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df = df.groupby('year').last().reset_index()[['date', 'index_value']]
        df['date'] = df['date'].dt.date
        df['index_name'] = name
        logger.info(f"Fetched {len(df)} yearly records for {name}")
        return df
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

def fetch_all_indices():
    dfs = []
    indices = {'^GSPC': 'SP500', '^DJI': 'DOW'}
    for ticker, name in indices.items():
        df = fetch_stock_index(ticker, name)
        if df is not None:
            dfs.append(df)
        time.sleep(1)
    if not dfs:
        return None
    result = pd.concat(dfs)
    result_pivot = result.pivot(index='date', columns='index_name', values='index_value').reset_index()
    result_pivot.columns = [col.lower() if col != 'date' else col for col in result_pivot.columns]
    return result_pivot

def save_data(df):
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/stock_indices.csv', index=False)
    logger.info(f"Saved {len(df)} records to CSV")
    connection_string = get_db_connection_string()
    df.to_sql('stock_indices', connection_string, if_exists='replace', index=False)
    logger.info("Data saved to PostgreSQL")

def main():
    logger.info("Fetching stock indices (yearly data)")
    df = fetch_all_indices()
    if df is not None and not df.empty:
        save_data(df)
        logger.info(f"Success: {len(df)} records, columns: {list(df.columns)}")
    else:
        logger.error("Failed to fetch data")

if __name__ == "__main__":
    main()

    