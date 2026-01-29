from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from utils_module.utils import test1, test2

with DAG(
    dag_id="demo_kubernetes_pod_operator",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "k8s", "kpo"],
) as dag:

    prereq_step = BashOperator(
        task_id="prereq_step",
        bash_command=f"echo test1={test1()} && date",
    )
    run_in_pod = KubernetesPodOperator(
        task_id="run_in_pod",
        name="demo-kpo-busybox",
        namespace="airflow",

        # since Airflow itself is running in the cluster (kind), use in_cluster
        in_cluster=True,  # :contentReference[oaicite:3]{index=3}

        # use the RBAC-enabled service account we created
        service_account_name="airflow-kpo",

        image="busybox:1.36",
        cmds=["sh", "-c"],
        arguments=["echo hello-from-kpo && echo test test test && sleep 3"],

        get_logs=True,
        is_delete_operator_pod=True,
    )

    prereq_step >> run_in_pod
