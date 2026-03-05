#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
echo "Testing connection with:"
echo "  Database: ${POSTGRES_DB}"
echo "  User: ${POSTGRES_USER}"
echo "  Host: ${POSTGRES_HOST}"
echo "  Port: ${POSTGRES_PORT}"

# Wait for PostgreSQL to be ready
until PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -p ${POSTGRES_PORT} -c '\q' 2>/dev/null; do
  echo "  PostgreSQL not ready, retrying in 2 seconds..."
  sleep 2
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