FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

ARG HOME_DIR=/src
WORKDIR $HOME_DIR

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev=3.9.2-3 \
        libpq-dev=13.9-0+deb11u1 \
        build-essential=12.9 \
    && pip install --no-cache-dir poetry==1.2.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker/scripts /scripts
COPY ./docker/bot/scripts /scripts
RUN chmod -R 777 /scripts

COPY ./pyproject.toml ./poetry.lock /
RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY ./bot/src .

ENTRYPOINT ["/scripts/entrypoint.sh"]
