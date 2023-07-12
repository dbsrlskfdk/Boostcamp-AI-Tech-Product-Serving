from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
        'owner': 'yungi',
        'depends_on_past' : False,
        'start_date' : datetime(2023, 7, 5),
        'retires' : 1,
        'retry_delay' : timedelta(minutes=5),
        }

def print_current_date():
    date_kor = ["월", "화", "수", "목", "금", "토", "일"]
    date_now = datetime.now().date()
    datetime_weeknum = date_now.weekday()
    print(f"{date_now}는 {date_kor[datetime_weeknum]}요일입니다")

with DAG(dag_id='python_dag1',
        default_args=default_args,
        schedule_interval="30 0 * * *", # UTC 시간 기준 0시 30분에 Daily로 실행하겠다. => 한국시간 기준 오전 9시 30분
        tags=['my_dags']) as dag:
    python_task = PythonOperator(
            task_id="print_current_date",
            python_callable=print_current_date)

