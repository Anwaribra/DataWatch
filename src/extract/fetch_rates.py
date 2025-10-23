import requests
import pandas as pd
import time
import logging
import json
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

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

    logger.info("Fetching USD/EGP data from Alpha Vantage...")
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

if __name__ == "__main__":
    df = fetch_usd_egp_historical()
    if df is not None:
        print(df.head())
