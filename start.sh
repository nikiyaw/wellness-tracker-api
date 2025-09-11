#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run Alembic migrations to create/update database tables
echo "Running database migrations..."
DATABASE_URL="postgresql+psycopg://wellness_tracker_db_n8nu_user:cEapNDJbZI9PXSwCHzMY3aCq0cmp1xvI@dpg-d314m3ndiees73ah6beg-a/wellness_tracker_db_n8nu" alembic upgrade head

# Start the application server
echo "Starting the application..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
