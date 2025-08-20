#!/bin/sh
set -e

# Export env for Alembic
export PYTHONPATH=/app

autoupgrade() {
  echo "Running alembic upgrade head..."
  alembic upgrade head || (echo "Alembic failed" && exit 1)
}

autoupgrade

exec uvicorn app.api.main:app --host 0.0.0.0 --port 12000
