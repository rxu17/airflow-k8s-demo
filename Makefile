CLUSTER_NAME=airflow-demo
NAMESPACE=airflow
RELEASE=airflow
IMAGE_REPO=airflow-k8s-demo
IMAGE_TAG=local
IMAGE=$(IMAGE_REPO):$(IMAGE_TAG)

kind-up:
	kind create cluster --name $(CLUSTER_NAME) --config kind/cluster.yaml

kind-down:
	kind delete cluster --name $(CLUSTER_NAME)

image-build:
	docker build -t $(IMAGE) .

kind-load:
	kind load docker-image $(IMAGE) --name $(CLUSTER_NAME)

helm-install:
	helm repo add apache-airflow https://airflow.apache.org
	helm repo update
	helm upgrade --install $(RELEASE) apache-airflow/airflow \
	  -n $(NAMESPACE) --create-namespace \
	  -f helm/values.yaml

helm-uninstall:
	helm uninstall $(RELEASE) -n $(NAMESPACE) || true

status:
	kubectl get pods -n $(NAMESPACE)

ui:
	@echo "Airflow UI: http://localhost:8080"
	@echo "If pods aren't ready yet, run: make status"
	@echo "To get admin password, run: make admin-password"

admin-password:
	@kubectl get secret -n $(NAMESPACE) $(RELEASE)-webserver-secret \
	  -o jsonpath='{.data.admin-password}' | base64 --decode; echo

rbac:
	kubectl apply -f k8s/airflow-kpo-rbac.yaml

pods:
	kubectl get pods -n airflow -w
