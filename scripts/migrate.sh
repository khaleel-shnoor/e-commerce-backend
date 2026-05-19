#!/usr/bin/env bash
# Run Alembic migrations (Linux/macOS)
set -euo pipefail
cd "$(dirname "$0")/.."

source .venv/bin/activate

if [[ "${1:-}" == "upgrade" ]]; then
  alembic upgrade head
else
  alembic revision --autogenerate -m "${1:-autogenerate}"
  echo "Review alembic/versions/, then: alembic upgrade head"
fi
