from datetime import datetime, date, timedelta
from io import BytesIO
from minio import Minio
import pathlib
import pandas as pd
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


def extract():
    # busca a lista de objetos no data lake.
    objects = client.list_objects('landing', recursive=True)

    # faz o download de cada arquivo e concatena com o dataframe vazio.
    for obj in objects:
        print("Downloading file...")
        print(obj.bucket_name, obj.object_name)

        client.fget_object(
            obj.bucket_name,
            obj.object_name,
            'temp/'+obj.object_name,
        )


def converte_parquet():
    # carrega os nomes de arquivos a partir de uma pasta.
    filename = os.listdir('temp')

    for obj in filename:
        # gera os datasets
        df = pd.read_csv("temp/"+obj, sep=',', header=0)
        # tira a extensao do nome do arquivo
        filenamemod = pathlib.Path(obj).stem
        # converte o dataset em parquet
        df.to_parquet(
            "parquet_saved/{}.parquet".format(filenamemod), index=False)

        # carrega os dados para o Data Lake.
        client.fput_object("processing", filenamemod+".parquet",
                           "parquet_saved/{}.parquet".format(filenamemod))


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
    'converte_csv_para_parquet',
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

    extract = PythonOperator(
        task_id="baixa_arquivo_bucket_landing",
        provide_context=True,
        python_callable=extract
    )

    converte_parquet = PythonOperator(
        task_id="transform_parquet_load",
        provide_context=True,
        python_callable=converte_parquet
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

    clean_folder_temp = BashOperator(
        task_id="limpeza_pasta_temp",
        bash_command="rm -r /opt/airflow/temp/*;"

    )
    clean_folder_parquet = BashOperator(
        task_id="limpeza_pasta_parquet",
        bash_command="rm -r /opt/airflow/parquet_saved/*;"
    )

    verifica_pasta >> eh_valida >> [com_dados, sem_dados]
    sem_dados >> send_email_notification
    com_dados >> extract >> converte_parquet >> clean_folder_temp >> clean_folder_parquet
