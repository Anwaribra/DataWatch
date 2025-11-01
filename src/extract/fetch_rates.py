import requests
import pandas as pd
import time
import logging
import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy  


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


def save_to_database(df):
    connection_string = get_db_connection_string()
    engine = create_engine(connection_string)
    
    df_to_save = df.copy()
    df_to_save = df_to_save.reset_index()
    df_to_save.columns = ['date', 'usd_egp_rate']
    df_to_save['date'] = pd.to_datetime(df_to_save['date']).dt.date
    
    with engine.begin() as conn:
        df_to_save.to_sql('usd_egp_rates', conn, if_exists='replace', index=False)
    
    logger.info("data saved to database")

config = load_config()
API_KEY = config['alpha_vantage']['api_key']
BASE_URL = config['alpha_vantage']['base_url']

def fetch_usd_egp_historical():
    params = {
        "function": "FX_DAILY",
        "from_symbol": "USD",
        "to_symbol": "EGP",
        "apikey": API_KEY,
        "outputsize": "full"  
    }

    logger.info("Fetching USD/EGP data from Alpha Vantage")
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series FX (Daily)" not in data:
        logger.error(f"Unexpected response: {data}")
        return None

    df = pd.DataFrame.from_dict(data["Time Series FX (Daily)"], orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # just close rate
    df = df.rename(columns={"4. close": "usd_egp_rate"})
    df = df[["usd_egp_rate"]].astype(float)

    df.to_csv("data/raw/usd_egp.csv")
    logger.info("done fetching usd_egp")
    return df

def main():
    df = fetch_usd_egp_historical()
    if df is not None:
        save_to_database(df)
        logger.info("fetching completed!")

if __name__ == "__main__":
    main()
