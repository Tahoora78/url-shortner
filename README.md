# URL Shortener — Docker usage

This repository contains a small FastAPI URL shortener.

Quick start with Docker Compose

1. Build and start services:

```bash
docker compose up --build
```

2. The API will be available at: `http://localhost:8000`

Notes
- The compose setup runs a `redis` service and a `web` service.
- The SQLite database file is persisted on the host at `./data/shortener.db`.
- On container start the entrypoint script waits for Redis, runs Alembic
  migrations (`alembic upgrade head`), and then starts `uvicorn`.

Environment variables
- `DATABASE_URL` — SQLAlchemy connection string (default: `sqlite:///./data/shortener.db`).
- `REDIS_HOST`, `REDIS_PORT` — Redis connection settings (defaults set in compose).

Production notes
- For production, prefer a managed database (Postgres) and set `DATABASE_URL`.
- Remove the bind mount `.:/app` in `docker-compose.yml` and rebuild the image for immutable deployments.
# URL Shortener Project (FastAPI)

Structure:
- app/: FastAPI application
  - main.py
  - database.py
  - models.py
  - crud.py
  - middleware.py
  - schemas.py
- alembic/: Alembic migrations
- SCALABILITY.md
- requirements.txt

Run:
- Install requirements: pip install -r requirements.txt
- Initialize DB (migrations): alembic upgrade head
- Start server: uvicorn app.main:app --reload
