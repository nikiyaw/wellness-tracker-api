#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run Alembic migrations to create/update database tables
echo "Running database migrations..."
alembic upgrade head

# Start the application server
echo "Starting the application..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT