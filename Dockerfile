# -------------------------------------
# DOCKERFILE (BASE)
# -------------------------------------
# NOTE: Create a container appropriate for Django and Django-Geo

FROM python:3.6

# NOTE: Update and install system dependencies
#       Django-Geo Libs: binutils, libproj-dev, gdal-bin, libgeoip1, python-gdal
#       Django-i18n Libs: gettext libgettextpo-dev
RUN apt-get update -y && apt-get install -y \
    apt-utils \
    # binutils \
    # libproj-dev \
    # gdal-bin \
    # libgeoip1 \
    # python3-gdal \
    gettext \
    libgettextpo-dev

# NOTE: Update and install Python dependencies
# TODO: Set poetry version as ENV
RUN pip install -U pip \
    && pip install poetry>=0.12 \
    && poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

# ENV Setup
# =====================================

# Single line form is preferred for caching
ENV PYTHONPATH=/usr/app/project \
    DJANGO_SETTINGS_MODULE=project.settings.local
    # WORKERS=$WORKERS

# Working Dir Setup
# =====================================
# We're about to work with the local context alot,
# let's make paths a little easir

WORKDIR /usr/app

# Install Dependencies
# =====================================a

COPY poetry.lock /usr/app
COPY pyproject.toml /usr/app

RUN poetry install --no-interaction --no-ansi --no-dev

# NOTE: Mostly everything that follows will invalidate the cache

# Copy Local Files
# =====================================

COPY manage.py manage.py
COPY project project


