FROM python:3.11

WORKDIR /app

COPY api/ ./api
COPY poetry.lock .
COPY pyproject.toml .
COPY Makefile .

RUN pip install poetry==1.3.0 \
    && poetry config virtualenvs.create false \
    && poetry install
