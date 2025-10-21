import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engineering.Dag_scheduler import create_csv, stocking_log, simulate_business_day
#NOTE: to get reference of the dates, you need to pass execution_date in the arguments

with DAG(
    dag_id='business_day_simulator',
    start_date=pendulum.datetime(2025, 9, 19, tz="America/New_York"),
    schedule='@daily',
    catchup=True,
    max_active_runs=1
) as dag:

    t1 = PythonOperator (
        task_id='create_csv',
        python_callable=create_csv,
        do_xcom_push=False
    )
    t2 = PythonOperator(
        task_id='alert_and_stock',
        python_callable=stocking_log,
        do_xcom_push=False
    )
    t3 = PythonOperator (
        task_id='simulate_business_day',
        python_callable=simulate_business_day,
        do_xcom_push=False
    )

    t1 >> t2 >> t3

