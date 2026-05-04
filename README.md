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
Ensure PostgreSQL is running and update the `DATABASE_URL` in `.env`.

### 3. Run Migrations
```bash
alembic upgrade head
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```
