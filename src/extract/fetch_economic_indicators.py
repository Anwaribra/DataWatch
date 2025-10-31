import requests
import pandas as pd
import logging
import json
import os
from datetime import datetime
from dotenv import load_dotenv

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
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return connection_string

def fetch_indicator(code, name):
    try:
        url = f"https://api.worldbank.org/v2/country/EG/indicator/{code}"
        params = {"format": "json", "date": "1960:2025", "per_page": 20000}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if not data or len(data) < 2 or not data[1]:
            return None
        
        records = [{'date': f"{entry['date']}-12-31", 'value': float(entry['value'])} 
                   for entry in data[1] if entry['value'] is not None]
        
        if not records:
            return None
        
        df = pd.DataFrame(records)
        df = df.rename(columns={'value': name})
        df['date'] = pd.to_datetime(df['date']).dt.date
        logger.info(f"Fetched {len(df)} records for {name}")
        return df
    except Exception as e:
        logger.error(f"Error fetching {name}: {e}")
        return None

def fetch_all():
    config = load_config()
    indicators = config.get('world_bank', {}).get('indicators', {})
    
    inflation = fetch_indicator(indicators['inflation'], 'inflation_rate')
    gdp = fetch_indicator(indicators['gdp_growth'], 'gdp_growth_rate')
    unemployment = fetch_indicator(indicators['unemployment'], 'unemployment_rate')
    
    result = inflation
    for df in [gdp, unemployment]:
        if df is not None:
            if result is not None:
                result = pd.merge(result, df, on='date', how='outer')
            else:
                result = df
    
    if result is not None:
        result = result.sort_values('date').reset_index(drop=True)
        result['source'] = 'world_bank'
    
    return result

def save_data(df):
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/economic_indicators.csv', index=False)
    logger.info(f"Saved {len(df)} records to CSV")
    
    connection_string = get_db_connection_string()
    df.to_sql('economic_indicators', connection_string, if_exists='replace', index=False)
    logger.info("data saved to postgres")

def main():
    logger.info("fetching economic indicators")
    df = fetch_all()
    if df is not None and not df.empty:
        save_data(df)
        logger.info(f"success: {len(df)} records")
    else:
        logger.error("failed to fetch data")

if __name__ == "__main__":
    main()