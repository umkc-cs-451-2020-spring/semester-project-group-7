#!/bin/bash -x

python manage.py migrate --noinput || exit 1
python manage.py collectstatic --noinput || exit 1

# celery worker -A commercebank --loglevel=info -B&
exec "$@"
