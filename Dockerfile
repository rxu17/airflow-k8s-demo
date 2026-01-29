FROM apache/airflow:2.11.0-python3.11

USER airflow

# Install your shared package (src/)
COPY pyproject.toml /opt/airflow/
COPY src/ /opt/airflow/src/
RUN pip install --no-cache-dir /opt/airflow

# Install Kubernetes provider (for KubernetesPodOperator / KubernetesExecutor)
RUN pip install --no-cache-dir apache-airflow-providers-cncf-kubernetes

# Copy DAGs into the image
COPY dags/ /opt/airflow/dags/
