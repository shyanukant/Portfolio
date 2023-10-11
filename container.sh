#!/bin/sh
set -e

# Get env vars in the Dockerfile to show up in the SSH session
eval $(printenv | sed -n "s/^\([^=]\+\)=\(.*\)$/export \1=\2/p" | sed 's/"/\\\"/g' | sed '/=/s//="/' | sed 's/$/"/' >> /etc/profile)

echo "Starting SSH ..."
service ssh start


COPY migrations /app/migrations

# Apply the migration
flask db upgrade

# Start Gunicorn
exec gunicorn --workers=4 --bind 0.0.0.0:5000 app:app