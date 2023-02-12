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
	python -m uvicorn main:app


.PHONY: swagger
swagger:
	open -a safari http://localhost:8000/docs


.PHONY: format
format:
	black .
