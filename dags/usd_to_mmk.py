from datetime import datetime
import logging

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

import requests
import json

default_args = {
    'owner': 'zayarphyo',
    'depends_on_past': False,
}

dag = DAG(
    dag_id='usd_to_mmk',
    start_date=datetime(2021, 1, 1),
    schedule_interval='*/1 * * * *', # '@once'
    default_args=default_args,
)

url = "https://forex.cbm.gov.mm/api/latest"
response = requests.get(url).text
data = json.loads(response)

templated_command = """
    echo 1 USD = {{ params.usd }} MMK
    echo last updated at {{ params.time }} from {{ params.info }}
"""


test = BashOperator(
    task_id='myTask',
    bash_command=templated_command,
    params={
        "info": data["info"],
        "time": datetime.fromtimestamp(int(data["timestamp"])),
        "usd": data["rates"]["USD"],
    },
    dag=dag,
)
