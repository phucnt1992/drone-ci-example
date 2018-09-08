FROM python:alpine3.6

COPY requirements/base.txt /requirements.txt

RUN set -ex \
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
    wget \
    && python3 -m venv /.pyenv \
    && /.pyenv/bin/pip install -U pip \
    && /.pyenv/bin/pip install --no-cache-dir -r /requirements.txt
    && rm -f requirements.txt

COPY config /config
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN ["chmod", "+x", "/docker-entrypoint.sh"]

WORKDIR /app
COPY example /app/

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD [ "/.pyenv/bin/uwsgi", "/config/uwsgi.ini"]
