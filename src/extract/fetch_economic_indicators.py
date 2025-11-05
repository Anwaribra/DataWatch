import requests
import pandas as pd
import logging
import json
import os
from datetime import datetime
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
    db_password = os.getenv('DB_PASSWORD','2003')
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def fetch_indicator(code, name):
    url = f"https://api.worldbank.org/v2/country/EG/indicator/{code}"
    params = {"format": "json", "date": "1960:2025", "per_page": 20000}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    records = [{'date': f"{entry['date']}-12-31", 'value': float(entry['value'])} 
               for entry in data[1] if entry['value'] is not None]
    
    df = pd.DataFrame(records)
    df = df.rename(columns={'value': name})
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df

def fetch_all():
    config = load_config()
    indicators = config.get('world_bank', {}).get('indicators', {})
    
    inflation = fetch_indicator(indicators['inflation'], 'inflation_rate')
    gdp = fetch_indicator(indicators['gdp_growth'], 'gdp_growth_rate')
    unemployment = fetch_indicator(indicators['unemployment'], 'unemployment_rate')
    
    result = inflation
    for df in [gdp, unemployment]:
        result = pd.merge(result, df, on='date', how='outer')
    
    result = result.sort_values('date').reset_index(drop=True)
    result['source'] = 'world_bank'
    
    return result

def save_data(df):
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, 'data', 'raw')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'economic_indicators.csv')
    df.to_csv(csv_path, index=False)
    
    engine = create_engine(get_db_connection_string())
    with engine.begin() as conn:
        df.to_sql('economic_indicators', conn, if_exists='replace', index=False)
    logger.info("Data saved to postgres")

def main():
    df = fetch_all()
    save_data(df)
    logger.info(f"Success: {len(df)} records")

if __name__ == "__main__":
    main()
