import logging
import sys
from datetime import datetime, timedelta

sys.path.append("/opt/airflow/f1_data_pipeline_airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.load.save_to_db import save_to_db
from src.load.load_dimensional_model import build_and_load_dimensional_model
from src.extract.f1_results_api import fetch_race_results, parse_race_results
from src.transform.build_analytics_marts import create_driver_season_stats

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

def save_raw_results_to_db():
    logger.info("Starting data ingestion from API")
    all_results = fetch_race_results("2025")

    logger.info("Parsing races results from API")
    df = parse_race_results(all_results)

    logger.info("Saving cleaned data to table 'raw_race_results'")
    save_to_db(df=df, table="raw_race_results")

    logger.info("Load step completed successfully")

def save_dim_data_to_db():
    logger.info("Starting save dimensional data to db")
    build_and_load_dimensional_model()
    logger.info("Save step completed successfully")

def save_analytics_marts_to_db():
    logger.info("Starting save analitycs marts to db")
    analytics_df = create_driver_season_stats()

    save_to_db(analytics_df, "driver_season_stats")

    logger.info("Save step completed successfully")

with DAG(
    dag_id='f1_raw_results_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args= default_args
)as dag:
    
    task_1 = PythonOperator(
        task_id="load_raw_results",
        python_callable=save_raw_results_to_db
    )
    task_2 = PythonOperator(
        task_id="save_dim_data_to_db",
        python_callable=save_dim_data_to_db
    )
    task_3 = PythonOperator(
        task_id="save_analitycs_marts_to_db",
        python_callable=save_analytics_marts_to_db
    )

    task_1 >> task_2 >> task_3