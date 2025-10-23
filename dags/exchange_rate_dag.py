# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.operators.bash import BashOperator
# from airflow.operators.email import EmailOperator
# from airflow.sensors.filesystem import FileSensor
# from airflow.models import Variable
# from datetime import datetime, timedelta
# import sys
# import os
# import pandas as pd
# from pathlib import Path

# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# from extract.fetch_exchange_rates import fetch_exchange_rates
# from extract.fetch_gold_silver_prices import fetch_gold_price


# default_args = {
#     'owner': 'EIS Team',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 1, 1),
#     'email_on_failure': True,
#     'email_on_retry': False,
#     'retries': 2,
#     'retry_delay': timedelta(minutes=5),
#     'email': ['admin@eis.com']
# }

# # Create DAG
# dag = DAG(
#     'economic_intelligence_system',
#     default_args=default_args,
#     description='Economic Intelligence System - Complete ETL Pipeline',
#     schedule_interval='0 */6 * * *',  
#     catchup=False,
#     max_active_runs=1,
#     tags=['rates', 'gold', 'silver', 'monitoring']
# )

# def extract_exchange_rates_task():
#     """Extract exchange rate data"""
#     try:
#         result = fetch_exchange_rates('USD', 'EGP')
#         if result:
#             print(f"Exchange rate extracted: {result['conversion_rate']}")
#             return result
#         else:
#             raise Exception("Failed to extract exchange rates")
#     except Exception as e:
#         print(f"Error extracting exchange rates: {e}")
#         raise

# def extract_gold_prices_task():
#     """Extract gold price data"""
#     try:
#         result = fetch_gold_price('USD', 'EGP')
#         if result:
#             print(f"Gold price extracted: {result['gold_price_per_ounce']}")
#             return result
#         else:
#             raise Exception("Failed to extract gold prices")
#     except Exception as e:
#         print(f"Error extracting gold prices: {e}")
#         raise







# def load_to_database_task():
#     """Load processed data to database"""
#     try:
#         db_manager = get_db_connection()
#         if not db_manager.connect():
#             raise Exception("Failed to connect to database")
        
#         # Load exchange rates
#         exchange_files = list(Path("data/processed").glob("exchange_rates_*.parquet"))
#         for file_path in exchange_files:
#             df = pd.read_parquet(file_path)
#             db_manager.insert_dataframe(df, 'exchange_rates')
        
#         # Load gold prices
#         gold_files = list(Path("data/processed").glob("gold_prices_*.parquet"))
#         for file_path in gold_files:
#             df = pd.read_parquet(file_path)
#             db_manager.insert_dataframe(df, 'gold_prices')
        
#         # Load economic indicators
#         indicator_files = list(Path("data/processed").glob("economic_indicators_*.parquet"))
#         for file_path in indicator_files:
#             df = pd.read_parquet(file_path)
#             db_manager.insert_dataframe(df, 'economic_indicators')
        
#         # Load news articles
#         news_files = list(Path("data/processed").glob("news_articles_*.parquet"))
#         for file_path in news_files:
#             df = pd.read_parquet(file_path)
#             db_manager.insert_dataframe(df, 'news_articles')
        
#         print("Data loaded to database successfully")
#         return "success"
        
#     except Exception as e:
#         print(f"Error loading data to database: {e}")
#         raise

# def send_success_notification():
#     """Send success notification"""
#     return "Pipeline completed successfully"

# def send_failure_notification():
#     """Send failure notification"""
#     return "Pipeline failed - check logs"

# # Define tasks
# extract_exchange_rates = PythonOperator(
#     task_id='extract_exchange_rates',
#     python_callable=extract_exchange_rates_task,
#     dag=dag
# )

# extract_gold_prices = PythonOperator(
#     task_id='extract_gold_prices',
#     python_callable=extract_gold_prices_task,
#     dag=dag
# )

# extract_economic_indicators = PythonOperator(
#     task_id='extract_economic_indicators',
#     python_callable=extract_economic_indicators_task,
#     dag=dag
# )

# extract_news_sentiment = PythonOperator(
#     task_id='extract_news_sentiment',
#     python_callable=extract_news_sentiment_task,
#     dag=dag
# )

# transform_data = PythonOperator(
#     task_id='transform_data',
#     python_callable=transform_data_task,
#     dag=dag
# )

# validate_data_quality = PythonOperator(
#     task_id='validate_data_quality',
#     python_callable=validate_data_quality_task,
#     dag=dag
# )

# load_to_database = PythonOperator(
#     task_id='load_to_database',
#     python_callable=load_to_database_task,
#     dag=dag
# )

# # Create data directory
# create_data_dirs = BashOperator(
#     task_id='create_data_directories',
#     bash_command='mkdir -p data/raw data/processed data/archive data/logs',
#     dag=dag
# )

# # Success notification
# success_notification = PythonOperator(
#     task_id='success_notification',
#     python_callable=send_success_notification,
#     trigger_rule='all_success',
#     dag=dag
# )

# # Failure notification
# failure_notification = PythonOperator(
#     task_id='failure_notification',
#     python_callable=send_failure_notification,
#     trigger_rule='one_failed',
#     dag=dag
# )

# # Define task dependencies
# create_data_dirs >> [extract_exchange_rates, extract_gold_prices, extract_economic_indicators, extract_news_sentiment]

# [extract_exchange_rates, extract_gold_prices, extract_economic_indicators, extract_news_sentiment] >> transform_data

# transform_data >> validate_data_quality

# validate_data_quality >> load_to_database

# load_to_database >> success_notification

# [extract_exchange_rates, extract_gold_prices, extract_economic_indicators, extract_news_sentiment, transform_data, validate_data_quality, load_to_database] >> failure_notification


