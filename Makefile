PYTHON_VERSION=3.11
VENV=.venv

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


.PHONY: upgrade
upgrade:
	alembic upgrade head

.PHONY: downgrade
downgrade:
	alembic downgrade -1
