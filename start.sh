#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run Alembic migrations to create/update database tables
echo "Running database migrations..."
DATABASE_URL="postgresql+psycopg://wellness_tracker_db_llvw_user:a0f0MPJZJkH2wSY5E9ncGgjR3QE0TKbN@dpg-d2togl7fte5s73aeoog0-a/wellness_tracker_db_llvw" alembic upgrade head

# Start the application server
echo "Starting the application..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
