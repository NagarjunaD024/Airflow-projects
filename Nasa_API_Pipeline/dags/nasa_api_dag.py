import json
import pathlib

import airflow
import requests
import requests.exceptions as request_exceptions
from datetime import date
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import datetime, timedelta 

dag_owner = 'Nagarjuna'

def _get_pictures(ds, **kwargs):
    # 1. Define the temporary directory
    output_dir = pathlib.Path("/tmp/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # NASA API Setup
    api_key = 'cKxoWLqd6CvbgVjPb42UpoIC4Yse2Re1IozfQysJ'
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    
    # It is better to fetch the image for the specific Airflow 'ds' (logical date)
    # but for simplicity, we use the URL from the API response
    response = requests.get(url).json()
    
    if 'hdurl' in response:
        image_url = response['hdurl']
        # 2. Define the full file path inside the temp folder
        # We use 'ds' from Airflow so backfills work correctly
        target_file = output_dir / f"todays_image_{ds}.png"
        
        # Download and save
        response_image = requests.get(image_url)
        with open(target_file, 'wb') as f:
            f.write(response_image.content)
        print(f"Stored image at: {target_file}")
    else:
        print("No HD image found in the API response today.")

default_args = {
    'owner': dag_owner,
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='download_ASOD_image',
    default_args=default_args,
    description='Download NASA APOD and notify',
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    tags=['NASA']
) as dag:

    get_pictures = PythonOperator(
        task_id="get_pictures",
        python_callable=_get_pictures,
    )

    notify = BashOperator(
        task_id="notify",
        # Using {{ ds }} to dynamically show the date in the message
        bash_command='echo "Images for {{ ds }} have been added to /tmp/images!"',
    )

    get_pictures >> notify