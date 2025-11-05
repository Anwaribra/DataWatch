import pandas as pd
import logging
import json
import os
from datetime import datetime, timedelta
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine

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

def save_to_database(df):
    engine = create_engine(get_db_connection_string())
    df_to_save = df.copy()
    df_to_save['date'] = pd.to_datetime(df_to_save['date']).dt.date
    with engine.begin() as conn:
        df_to_save.to_sql('metals_prices', conn, if_exists='replace', index=False)
    logger.info("Data saved to database")

def fetch_yahoo_finance_data():
    gold_ticker = yf.Ticker("GC=F")
    silver_ticker = yf.Ticker("SI=F")
    start_date = "2020-01-01"
    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    gold_data = gold_ticker.history(start=start_date, end=end_date)
    silver_data = silver_ticker.history(start=start_date, end=end_date)
    
    gold_prices = gold_data['Close'].reset_index()
    silver_prices = silver_data['Close'].reset_index()
    gold_prices.columns = ['date', 'gold_price_usd']
    silver_prices.columns = ['date', 'silver_price_usd']
    merged_data = pd.merge(gold_prices, silver_prices, on='date', how='outer')
    merged_data['source'] = 'yahoo_finance'
    return merged_data

def fetch_gold_silver_prices():
    data = fetch_yahoo_finance_data()
    data = data.sort_values('date').reset_index(drop=True)
    data['gold_price_usd'] = data['gold_price_usd'].interpolate(method='linear')
    data['silver_price_usd'] = data['silver_price_usd'].interpolate(method='linear')
    return data

def save_prices_to_csv(df, filename):
    os.makedirs('data/raw', exist_ok=True)
    filepath = f'data/raw/{filename}'
    df.to_csv(filepath, index=False)
    return filepath

def main():
    historical_prices = fetch_gold_silver_prices()
    save_prices_to_csv(historical_prices, 'gold_silver_prices.csv')
    save_to_database(historical_prices)
    logger.info("Fetching completed!")

if __name__ == "__main__":
    main()
