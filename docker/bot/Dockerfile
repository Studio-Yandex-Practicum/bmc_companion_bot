FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

ARG HOME_DIR=/src
WORKDIR $HOME_DIR

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY ./docker/scripts /scripts
COPY ./docker/bot/scripts /scripts
RUN chmod -R 777 /scripts

COPY ./pyproject.toml ./poetry.lock /
RUN poetry config virtualenvs.create false \
    && poetry install --only main,bot

COPY ./bot/src .

ENTRYPOINT ["/scripts/entrypoint.sh"]
