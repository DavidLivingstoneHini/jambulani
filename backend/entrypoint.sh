#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -p ${POSTGRES_PORT} -c '\q' 2>/dev/null; do
  echo "  PostgreSQL not ready, retrying in 2 seconds..."
  sleep 2
done
echo "PostgreSQL ready."

echo "Waiting for Redis..."
# Simple approach - just ping Redis on the default host and port
until redis-cli -h redis -p 6379 ping 2>/dev/null | grep -q "PONG"; do
  echo "  Redis not ready, retrying in 2 seconds..."
  sleep 2
done
echo "Redis ready."

# Make migrations if needed
python manage.py makemigrations --noinput

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Seed data (only if database is empty)
python manage.py seed_data

# Create cache table
python manage.py createcachetable

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --max-requests 1000 \
    --max-requests-jitter 50