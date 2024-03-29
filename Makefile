PYTHON_VERSION=3.11
VENV=.venv


include .test.env
export


.PHONY: init
init:
	python$(PYTHON_VERSION) -m venv $(VENV)
	echo --- EXECUTE THE NEXT LINE ---
	echo source $(VENV)/bin/activate


.PHONY: install
install:
	poetry install


.PHONY: run
run:
	python -m uvicorn api.main:app --reload


.PHONY: docker-build
docker-build:
	docker-compose build --no-cache --progress=plain


.PHONY: docker-up
docker-up:
	docker-compose up


.PHONY: api-up
api-up:
	docker-compose up -d api db grafana prometheus


.PHONY: lb-up
lb-up:
	docker-compose up nginx


.PHONY: swagger
swagger:
	open -a safari http://localhost:8000/docs


.PHONY: format
format:
	python -m black .


.PHONY: test
test:
	python -m pytest -l


.PHONY: kube-init
kube-init:
	echo EXECUTE: 'eval $(minikube docker-env)'


.PHONY: kube-rm
kube-rm:
	kubectl delete pod bacapibara-api


.PHONY: kube-run
kube-run:
	kubectl run bacapibara-api --image=bacapibara_api:latest --port=8000 --image-pull-policy=Never --command -- python3 -m uvicorn api.main:app --host 0.0.0.0


.PHONY: revision
revision:
	alembic revision --autogenerate -m ${MSG}


.PHONY: upgrade
upgrade:
	alembic upgrade head


.PHONY: downgrade
downgrade:
	alembic downgrade -1


.PHONY: cert
cert:
	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyut key.pem -days 365


.PHONY: fqdn
fqdn:
	echo "" >>  /etc/hosts && echo "127.0.0.1 irusla.nd" >> /etc/hosts


.PHONY: locust
locust:
	locust -H https://irusla.nd


.PHONY: consumer
consumer:
	python -m api.announcements


.PHONY: docker-consumer
docker-consumer:
	docker-compose up consumer


.PHONY: bot
bot:
	python -m bot

