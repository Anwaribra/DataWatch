import requests
import pandas as pd
import logging
import json
import os
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

def save_to_database(df):
    engine = create_engine(get_db_connection_string())
    df_to_save = df.copy().reset_index()
    df_to_save.columns = ['date', 'usd_egp_rate']
    df_to_save['date'] = pd.to_datetime(df_to_save['date']).dt.date
    with engine.begin() as conn:
        df_to_save.to_sql('exchange_rates', conn, if_exists='replace', index=False)
    logger.info("Data saved to database")

config = load_config()
API_KEY = config['alpha_vantage']['api_key']
BASE_URL = config['alpha_vantage']['base_url']

def fetch_latest_exchange_rate():
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "USD",
        "to_currency": "EGP",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()
    rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    last_refreshed = pd.to_datetime(data["Realtime Currency Exchange Rate"]["6. Last Refreshed"])
    return rate, last_refreshed.date()

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

    df = pd.DataFrame.from_dict(data["Time Series FX (Daily)"], orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.rename(columns={"4. close": "usd_egp_rate"})
    df = df[["usd_egp_rate"]].astype(float)

    df.to_csv("data/raw/usd_egp.csv")
    logger.info("Done fetching usd_egp")
    return df

def main():
    df = fetch_usd_egp_historical()
    save_to_database(df)
    logger.info("Fetching completed!")

if __name__ == "__main__":
    main()
