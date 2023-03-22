from datetime import datetime
from airflow.utils.task_group import TaskGroup
from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator

with DAG(dag_id="test_dag_with_no_tags", default_args={"start_date": datetime(2023, 3, 21)}, schedule_interval='@once') as dag:
    with TaskGroup('TaskGroupA') as TaskGroupA:
        for i in range(3):
            DummyOperator(task_id=f"test_task_a{i}")
    with TaskGroup('TaskGroupB') as TaskGroupB:
        for i in range(3):
            dateleft='{{macros.ds_add(ds,'+f'{i+1}'+')}}'
            BashOperator(task_id=f"test_task_b{i}",bash_command=f'echo {dateleft}')
    TaskGroupA >> TaskGroupB