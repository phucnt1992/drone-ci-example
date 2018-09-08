#!/bin/sh

set -ex \
    && apk --update add --no-cache \
    gcc \
    make \
    libc-dev \
    musl-dev \
    linux-headers \
    pcre-dev \
    python3-dev \
    libpq \
    postgresql-dev \

pip install -U pip setuptools wheel
pip install -r requirements/base.txt -r requirements/test.txt
