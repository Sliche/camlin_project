#!/bin/bash

# Example commands
echo "Starting application..."

alembic revision --autogenerate -m "Performing auto migration"
alembic upgrade head

export PYTHONPATH="/camlin:$PYTHONPATH"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 --reload

