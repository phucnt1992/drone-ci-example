#!/bin/sh
set -e

/.pyenv/bin/python /app/manage.py createcachetable

/.pyenv/bin/python /app/manage.py collectstatic --noinput

/.pyenv/bin/python /app/manage.py migrate --noinput

exec "$@"
