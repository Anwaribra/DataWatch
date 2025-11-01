from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'EIS pipeline',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
    'email_on_failure': False,
    'email_on_retry': False,
}

PROJECT_PATH = "/opt/airflow"
PY = "python"

with DAG(
    dag_id='eis_pipeline',
    start_date=datetime(2025, 10, 30),
    schedule='@daily',
    catchup=False,
    default_args=default_args,
) as dag:

    start = EmptyOperator(task_id='start')

    extract_usd_egp_rates = BashOperator(
        task_id='extract_usd_egp_rates',
        bash_command=f'{PY} src/extract/fetch_rates.py',
        cwd=PROJECT_PATH,
    )

    extract_economic_indicators = BashOperator(
        task_id='extract_economic_indicators',
        bash_command=f'{PY} src/extract/fetch_economic_indicators.py',
        cwd=PROJECT_PATH,
    )

    extract_gold_silver_prices = BashOperator(
        task_id='extract_gold_silver_prices',
        bash_command=f'{PY} src/extract/fetch_gold_silver_prices.py',
        cwd=PROJECT_PATH,
    )

    extract_stock_indices = BashOperator(
        task_id='extract_stock_indices',
        bash_command=f'{PY} src/extract/fetch_stock_indices.py',
        cwd=PROJECT_PATH,
    )

    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command=f'{PY} -m dbt seed --profiles-dir "{PROJECT_PATH}"',
        cwd=f'{PROJECT_PATH}/src/transform/datawatch',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'{PY} -m dbt run --profiles-dir "{PROJECT_PATH}"',
        cwd=f'{PROJECT_PATH}/src/transform/datawatch',
    )

    soda_scan_all = BashOperator(
        task_id='soda_scan_all',
        bash_command=f'{PY} -m soda scan -d database quality/checks.yml',
        cwd=PROJECT_PATH,
    )

    notify_success = EmptyOperator(task_id='notify_success')

    # pipeline steps
    start >> [
        extract_usd_egp_rates,
        extract_economic_indicators,
        extract_gold_silver_prices,
        extract_stock_indices
    ] >> dbt_seed >> dbt_run >> soda_scan_all >> notify_success
