#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until python -c "import psycopg2; psycopg2.connect(
    dbname='${POSTGRES_DB}',
    user='${POSTGRES_USER}',
    password='${POSTGRES_PASSWORD}',
    host='${POSTGRES_HOST}',
    port='${POSTGRES_PORT}'
)" 2>/dev/null; do
  echo "  PostgreSQL not ready, retrying..."
  sleep 1
done
echo "PostgreSQL ready."

# Make migrations if needed
python manage.py makemigrations --noinput

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Seed data (only if database is empty)
python manage.py seed_data

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
