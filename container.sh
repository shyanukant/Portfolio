#!/bin/sh
set -e
COPY migrations /app/migrations

# Apply the migration
flask db upgrade

# Start Gunicorn
exec gunicorn --workers=4 --bind 0.0.0.0:5000 app:app