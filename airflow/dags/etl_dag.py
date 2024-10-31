from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='A simple ETL pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    submit_flink_job = BashOperator(
        task_id='submit_flink_job',
        bash_command='docker-compose exec flink-jobmanager flink run -py ./jobs/etl.py',
    )

