from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from demo_shared.util import meaning_of_life

with DAG(
    dag_id="demo_kubernetes_pod_operator",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "k8s", "kpo"],
) as dag:

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
        arguments=["echo hello-from-kpo && echo meaning_of_life_is_42 && sleep 3"],

        get_logs=True,
        is_delete_operator_pod=True,
    )

    run_in_pod()
