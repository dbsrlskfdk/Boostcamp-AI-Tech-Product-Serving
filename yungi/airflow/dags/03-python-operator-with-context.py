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

def print_current_date_with_context_variable(*args, **kwargs):
    """
    {'conf': <airflow.configuration.AirflowConfigParser object at 0x7fccd0768f40>,
    'dag': <DAG: python_dag_with_context>,
    'dag_run': <DagRun python_dag_with_context @ 2023-07-07 00:30:00+00:00: scheduled__2023-07-07T00:30:00+00:00,
    externally triggered: False>,
    'data_interval_end': DateTime(2023, 7, 8, 0, 30, 0, tzinfo=Timezone('UTC')),
    'data_interval_start': DateTime(2023, 7, 7, 0, 30, 0, tzinfo=Timezone('UTC')),
    'ds': '2023-07-07',
    'ds_nodash': '20230707',
    """
    print(f"kwargs : {kwargs}")
    execution_date = kwargs['ds']
    execution_date_nodash = kwargs['ds_nodash']
    print(f"execution_date_nodash : {execution_date_nodash}")
    execution_date = datetime.strptime(execution_date, "%Y-%m-%d").date()
    date_kor = ["월", "화", "수", "목", "금", "토", "일"]
    datetime_weeknum = execution_date.weekday()
    print(f"{execution_date}는 {date_kor[datetime_weeknum]}요일입니다.")

with DAG(
        dag_id="python_dag_with_context",
        default_args=default_args,
        schedule_interval="30 0 * * *",
        tags=['my_dags']) as dag:
    PythonOperator(
            task_id="print_current_date_with_context_variable",
            python_callable=print_current_date_with_context_variable,
            provide_context=True # True일 경우에 airflow task Instance의 Attribute를 Keyword Argument로 Python 함수에서 사용 가능
            )
