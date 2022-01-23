from datetime import datetime, date, timedelta
from io import BytesIO
from minio import Minio
import glob
import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable



DEFAULT_ARGS = {
    'owner': 'PSergios',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 13),
}

data_lake_server = Variable.get("data_lake_server")
data_lake_login = Variable.get("data_lake_login")
data_lake_password = Variable.get("data_lake_password")


client = Minio(
    data_lake_server,
    access_key=data_lake_login,
    secret_key=data_lake_password,
    secure=False
)


with DAG(
    'analise_dados',
    default_args=DEFAULT_ARGS,
    description='DAG para analise de dados dos datasets',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    dummy_task = DummyOperator(
        task_id="dummy_task",
        # ui_color='#e8f7e4'
    )
