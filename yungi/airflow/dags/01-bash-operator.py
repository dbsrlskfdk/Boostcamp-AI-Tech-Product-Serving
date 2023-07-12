from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
        'owner': 'yungi',
        'depends_on_past' : False,
        'start_date' : datetime(2023, 7, 12),
        'retires' : 1,
        'retry_delay' : timedelta(minutes=5),
        }

with DAG(
        dag_id="bash_dag",
        default_args=default_args,
        schedule_interval="@once",
        tags=['my_dags']
        ) as dag:
    task1 = BashOperator(
            task_id="print_date",
            bash_command="date")
    
    task2 = BashOperator(
            task_id="sleep",
            bash_command="sleep 5",
            retries=2)

    task3 = BashOperator(
            task_id="pwd",
            bash_command="pwd")

    task1 >> task2 # task1 이후에 task2 수행
    task1 >> task3 # task1 이후에 task3 수행(2와 3을 병렬로 실행)
