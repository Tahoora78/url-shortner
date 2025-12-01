#!/usr/bin/env bash
set -euo pipefail

REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}

echo "Waiting for Redis at ${REDIS_HOST}:${REDIS_PORT}..."
python - <<PY
import socket,os,time,sys
host=os.environ.get('REDIS_HOST','redis')
port=int(os.environ.get('REDIS_PORT',6379))
for i in range(60):
    try:
        s=socket.create_connection((host, port), timeout=1)
        s.close()
        print('Redis reachable')
        sys.exit(0)
    except Exception:
        time.sleep(1)
print('Could not connect to Redis', file=sys.stderr)
sys.exit(1)
PY

echo "Running database migrations (alembic)..."
alembic upgrade head || true

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
