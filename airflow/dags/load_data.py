from airflow import DAG
from airflow.decorators import dag, task
import datetime
import os
import sys
sys.path.append('/opt/airflow/helper')

from helper import _load_to_fact_table, _export_fact_table

default_args = {
    'start_date':datetime.datetime(2023,9,23)
}

# Create DAG
@dag(dag_id='load_data', default_args=default_args, catchup=False, schedule_interval='*/5 * * * *')
def load_data():

    # Task #1 - Incrementally load data from postgres to bigquery
    @task
    def load_to_fact_table():
        _load_to_fact_table()


    load_to_fact_table() 


# Execute DAG
dag = load_data()
