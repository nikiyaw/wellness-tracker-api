#!/bin/bash

# Run database migration
echo "Running Alembic migrations..."
alembic upgrade head

# Start the Uvicorn server
echo "Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 10000
