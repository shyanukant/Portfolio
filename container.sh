#!/bin/sh
set -e

# Initialize and create an initial migration
flask db init
flask db migrate -m "initial migration"

# Apply the migration
flask db upgrade

# Start Gunicorn
exec gunicorn --workers=4 --bind 0.0.0.0:5000 app:app