# URL Shortener

Lightweight FastAPI-based URL shortener service. Includes DB migrations (Alembic), Docker support, and tests.

**Status:** Minimal project scaffold — run locally or with Docker.

**Contents:** `app/` (FastAPI app & DB models), `alembic/` (migrations), `tests/` (pytest).

**Prerequisites**
- Python 3.9+ (or the version in `requirements.txt`)
- `git`, optionally Docker & Docker Compose

**Local setup**
1. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy environment variables (example):
```bash
cp .env.example .env
# Edit .env to set DB URL and any secrets
```

**Database migrations**
- Initialize / run migrations with Alembic:
```bash
alembic upgrade head
```

**Run locally**
```bash
uvicorn app.main:app --reload
# or if you prefer: python -m app.main
```

**Docker**
- Build and run with Compose:
```bash
docker-compose up --build
```

**Tests**
```bash
pytest -q
```

**Useful git commands**
- To ensure `.gitignore` takes effect for already-tracked files:
```bash
git add .gitignore
git rm -r --cached .
git add .
git commit -m "Apply .gitignore"
```

**Contributing**
- Open an issue or PR. Keep changes small and focused; add tests where appropriate.

**Contact**
- Project owner: `https://github.com/Tahoora78`
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
  - schemas.py
  - logging.py
  - increment-runner.py
- alembic/: Alembic migrations
- SCALABILITY.md
- requirements.txt

Run:
- Install requirements: pip install -r requirements.txt
- Initialize DB (migrations): alembic upgrade head
- Start server: uvicorn app.main:app --reload
