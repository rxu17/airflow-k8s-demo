from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

from utils_module.utils import test1, test2


with DAG(
    dag_id="airflow_k8s_demo_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "k8s"],
) as dag:
    BashOperator(
        task_id="print_shared_code_values",
        bash_command=(
            f"echo {test2('airflow')} && "
            f"echo test1={test1()} && "
            "date"
        ),
    )
