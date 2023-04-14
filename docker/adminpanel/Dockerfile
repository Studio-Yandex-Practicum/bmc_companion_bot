FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

WORKDIR /BMC

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev=3.9.2-3 \
        libpq-dev=13.9-0+deb11u1 \
        build-essential=12.9 \
     && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip wheel setuptools --no-cache-dir \
    && pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY ./docker/scripts /scripts
COPY ./docker/adminpanel/scripts /scripts
RUN chmod -R 777 /scripts

COPY ./pyproject.toml ./poetry.lock /
RUN poetry config virtualenvs.create false \
    && poetry install --only adminpanel  \
    && poetry remove psycopg2-binary \
    && poetry add psycopg2

COPY ./adminpanel/src .
