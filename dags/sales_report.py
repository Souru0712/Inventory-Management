import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engineering.Dag_scheduler import sales_report

with DAG(
    dag_id='sales_report',
    start_date=pendulum.datetime(2025, 9, 19, tz="America/New_York"),
    schedule='@daily',
    catchup=True,
) as dag:

    t1 = PythonOperator (
        task_id='sales_report',
        python_callable=sales_report
    )

    t1