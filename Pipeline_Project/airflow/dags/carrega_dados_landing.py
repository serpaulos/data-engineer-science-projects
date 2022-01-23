from datetime import datetime, date, timedelta
from io import BytesIO
from minio import Minio
import glob
import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from airflow.operators.email import EmailOperator


DEFAULT_ARGS = {
    'owner': 'PSergios',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 13),
}

data_lake_server = Variable.get("data_lake_server")
data_lake_login = Variable.get("data_lake_login")
data_lake_password = Variable.get("data_lake_password")

# database_server = Variable.get("database_server")
# database_login = Variable.get("database_login")
# database_password = Variable.get("database_password")
# database_name = Variable.get("database_name")

client = Minio(
    data_lake_server,
    access_key=data_lake_login,
    secret_key=data_lake_password,
    secure=False
)


def upload_file():
    folder_path = 'data'
    bucket = 'landing'

    # extrair e salva em uma lista todo os nomes de arquivos dentro de uma pasta
    filename = os.listdir(folder_path)

    # faz upload de todos os arquivos de uma pasta para o bucket selecionado
    for files in filename:
        client.fput_object(bucket, files, folder_path+'/'+files)


def verifica_pasta():
    if len(os.listdir('data')) == 0:
        pasta = 'pasta vazia'
        return pasta


def eh_valida(ti):
    pasta = ti.xcom_pull(task_ids='verifica_pasta')
    if(pasta == 'pasta vazia'):
        return 'sem_dados'
    return 'com_dados'


with DAG(
    'etl_carrega_bucket_landing',
    default_args=DEFAULT_ARGS,
    description='DAG para processamento de um pipeline de dados',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    verifica_pasta = PythonOperator(
        task_id='verifica_pasta',
        python_callable=verifica_pasta
    )

    eh_valida = BranchPythonOperator(
        task_id="eh_valida",
        python_callable=eh_valida
    )

    upload_file = PythonOperator(
        task_id="upload_arquivo_bucket",
        provide_context=True,
        python_callable=upload_file
    )

    sem_dados = BashOperator(
        task_id='sem_dados',
        bash_command="echo 'Nao tinha dados'"
    )

    com_dados = BashOperator(
        task_id='com_dados',
        bash_command="echo 'Tinha dados'"
    )

    send_email_notification = EmailOperator(
        task_id='send_email_notification',
        to="pauloapost@mgmail.com",
        subject="etl_carrega_bucket_landing",
        html_content="<h3>etl_carrega_bucket_landing</h3>"
    )

    clean_task = BashOperator(
        task_id="limpeza_pasta_data",
        bash_command="rm -r /opt/airflow/data/*;"
    )

    verifica_pasta >> eh_valida >> [com_dados, sem_dados]
    sem_dados >> send_email_notification
    com_dados >> upload_file >> clean_task
