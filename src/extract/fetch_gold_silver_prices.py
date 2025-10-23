# import requests
# import pandas as pd
# import time
# import logging
# import json
# import os
# from datetime import datetime, timedelta

# # Logging setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load configuration
# def load_config():
#     config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
#     with open(config_path, 'r') as f:
#         return json.load(f)

# config = load_config()
# API_KEY = config['metalprice_api']['api_key']
# BASE_URL = config['metalprice_api']['base_url']

# def fetch_metal_price_for_date(date_str):
#     """Fetch metal prices for a specific date."""
#     params = {
#         "api_key": API_KEY,
#         "base": "USD",
#         "currencies": "EGP,XAU,XAG"
#     }

#     url = f"{BASE_URL}/{date_str}"
#     response = requests.get(url, params=params)

#     if response.status_code != 200:
#         logger.error(f"{date_str}: HTTP {response.status_code} - {response.text}")
#         return None

#     data = response.json()
#     rates = data.get("rates", {})

#     if not all(k in rates for k in ["EGP", "XAU", "XAG"]):
#         logger.warning(f"{date_str}: Missing rates - {rates}")
#         return None

#     usd_to_egp = rates["EGP"]
#     gold_usd = rates["XAU"]
#     silver_usd = rates["XAG"]

#     # Convert gold/silver from USD to EGP
#     gold_egp = (1 / gold_usd) * usd_to_egp
#     silver_egp = (1 / silver_usd) * usd_to_egp

#     return {
#         "date": date_str,
#         "usd_to_egp": usd_to_egp,
#         "gold_usd": gold_usd,
#         "silver_usd": silver_usd,
#         "gold_egp": gold_egp,
#         "silver_egp": silver_egp
#     }

# def fetch_historical_data(start_year=2015, end_year=2025):
#     """Fetch historical metal prices daily between two years."""
#     start_date = datetime(start_year, 1, 1)
#     end_date = datetime(end_year, 12, 31)

#     all_data = []
#     total_days = (end_date - start_date).days + 1

#     logger.info(f"Fetching metal prices from {start_year} to {end_year}...")

#     for i in range(total_days):
#         date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
#         record = fetch_metal_price_for_date(date_str)
#         if record:
#             all_data.append(record)

#         # Respect API rate limits (adjust if needed)
#         time.sleep(1.5)

#         if (i + 1) % 50 == 0:
#             logger.info(f"Fetched {i + 1} / {total_days} days...")

#     if not all_data:
#         logger.error("No data fetched!")
#         return None

#     df = pd.DataFrame(all_data)
#     os.makedirs("data/raw", exist_ok=True)
#     output_path = "data/raw/metal_prices_historical.csv"
#     df.to_csv(output_path, index=False)

#     logger.info(f"✅ Done! Saved {len(df)} records to {output_path}")
#     return df

# if __name__ == "__main__":
#     df = fetch_historical_data()
#     if df is not None:
#         print(df.head())
