from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

smtp_user = 'nandu143.gottipati@gmail.com'

def print_hello():
    return 'Hello World!'

default_args = {
    'owner': 'Nagarjuna',
    'start_date': days_ago(1),
    'email_on_failure': True
}

with DAG(
    dag_id = 'email_alert_example',
    schedule_interval = None,
    default_args = default_args
) as dag:

    email = EmailOperator(
        task_id = 'email_alert',
        to = 'nandu143.gottipati@gmail.com',
        subject = 'Airflow Pipeline Success:',
        html_content = """ <h3>Pipeline Execution Successful</h3>""",
        dag=dag
    )

    dummy_operator = DummyOperator(
        task_id = 'dummy_task',
        retries = 3,
        dag = dag
    )

    hello_operator = PythonOperator(
        task_id = 'hello_task',
        python_callable = print_hello,
        dag = dag
    )

    email >> dummy_operator >> hello_operator