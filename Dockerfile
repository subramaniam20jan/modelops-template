FROM python:3.10-slim

# RUN apt-get update -y && apt-get install gfortran libopenblas-dev liblapack-dev

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml /app/
COPY src/ /app/src/

RUN poetry install