from airflow import DAG
import datetime
import pendulum
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from function.game_result_crawling import game_result, game_detail_result

with DAG(
    dag_id = "dags_game_result",
    schedule = "59 23 * * *",
    start_date = pendulum.datetime(2024, 3, 1, tz = "Asia/Seoul"),
    catchup = False
) as dag:
    
    task_extract_game_result = PythonOperator(
        task_id = 'task_extract_game_result',
        python_callable = game_result
    )

    task_extract_game_detail_result = PythonOperator(
        task_id = 'task_extract_game_detail_result',
        python_callable = game_detail_result
    )
    
    task_extract_game_result >> task_extract_game_detail_result