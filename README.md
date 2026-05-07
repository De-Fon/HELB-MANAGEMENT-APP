# FastAPI Backend Scaffold

This repository contains the foundational scaffolding for a scalable FastAPI backend using PostgreSQL, strictly adhering to the feature-based architecture principles outlined in `AGENTS.md`.

## Features
- **Feature-Based Architecture**: Separation into `core/`, `apps/`, and `shared/` for explicit bounded contexts.
- **Strict Layering**: Enforced separation of Route, Service, Repository, and Database models.
- **SQLAlchemy & Alembic**: ORM and migration setup.
- **Pydantic Settings**: Type-safe configuration from `.env`.
- **Passlib & JWT**: Utilities ready for auth implementation.

## Project Structure
```text
.
├── alembic/              # Database migrations
├── alembic.ini
├── app/
│   ├── apps/             # Feature apps (e.g., users, products)
│   ├── core/             # Core settings, db setup, security
│   ├── shared/           # Shared utilities
│   └── main.py           # Application entry point
├── requirements.txt
├── .env
├── LOGGING.md            # Logging system documentation
└── README.md
```

## Setup & Run

### 1. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Database
Ensure PostgreSQL is running and update `DATABASE_URL`, `JWT_SECRET`, and `SMS_API_KEY` in `.env`.

### 3. Configure Redis
Ensure Redis is running and set `REDIS_URL` plus `REDIS_RATE_LIMIT_URL` in `.env`.
The rate limiter uses `REDIS_RATE_LIMIT_URL` so throttling keys stay separate from Celery or other Redis data.

### 4. Run Migrations
```bash
alembic upgrade head
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload
```
