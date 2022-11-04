FROM python:3.10.6-slim as python-base

ARG DEBIAN_FRONTEND=noninteractive
LABEL maintainer="Gleb Glushkov <ptjexio@gmail.com>"

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.2.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base as requirements-stage
# Install build dependencies.
RUN apt-get update \
 && apt-get install --no-install-recommends --assume-yes \
 build-essential \
 curl \
 git

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN curl -sSL https://install.python-poetry.org/ | python3 - --version $POETRY_VERSION

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes --no-interaction --no-ansi --output=requirements.txt && \
    poetry export --without-hashes --no-interaction --no-ansi --with dev --output=requirements-dev.txt
RUN pip install --prefix=/runtime --disable-pip-version-check --no-deps --force-reinstall -r requirements.txt

###############################################
# Production Image
###############################################
FROM python-base as production
COPY --from=requirements-stage /runtime /usr/local


COPY . /app/
ENV PYTHONPATH=/app