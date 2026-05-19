#!/usr/bin/env bash
# Render build script — install deps and run migrations
set -euo pipefail

pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
