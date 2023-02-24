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
