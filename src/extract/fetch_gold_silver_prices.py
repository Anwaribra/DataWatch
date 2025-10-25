import requests
import pandas as pd
import logging
import json
import os
from datetime import datetime, date, timedelta
import time
import yfinance as yf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def fetch_yahoo_finance_data():
    logger.info("fetching data from yahoo finance")
    
    gold_ticker = yf.Ticker("GC=F")
    silver_ticker = yf.Ticker("SI=F")
    
    start_date = "2025-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    gold_data = gold_ticker.history(start=start_date, end=end_date)
    silver_data = silver_ticker.history(start=start_date, end=end_date)
    
    gold_prices = gold_data['Close'].reset_index()
    silver_prices = silver_data['Close'].reset_index()
    
    gold_prices.columns = ['date', 'gold_price_usd']
    silver_prices.columns = ['date', 'silver_price_usd']
    
    merged_data = pd.merge(gold_prices, silver_prices, on='date', how='outer')
    merged_data['source'] = 'yahoo_finance'
    
    logger.info("done fetched")
    return merged_data

def fetch_gold_silver_prices_2025():
    logger.info("done fetched")
    
    data = fetch_yahoo_finance_data()
    data = data.sort_values('date').reset_index(drop=True)
    data['gold_price_usd'] = data['gold_price_usd'].interpolate(method='linear')
    data['silver_price_usd'] = data['silver_price_usd'].interpolate(method='linear')
    
    return data

def save_prices_to_csv(df, filename):
    os.makedirs('data/raw', exist_ok=True)
    
    filepath = f'data/raw/{filename}'
    df.to_csv(filepath, index=False)
    logger.info(f"Prices saved to {filepath}")
    return filepath

def main():
    historical_prices = fetch_gold_silver_prices_2025()
    save_prices_to_csv(historical_prices, 'gold_silver_prices.csv')
    logger.info("fetching completed!")


if __name__ == "__main__":
    main() 