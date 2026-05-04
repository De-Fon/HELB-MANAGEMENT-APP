# Project Commands Reference

This file contains every command you might need to run for this project, categorised and commented out for safe reference.

## 1. Environment & Setup
```bash
# Create a virtual environment
# python -m venv venv

# Activate the virtual environment (Linux/macOS)
# source venv/bin/activate

# Activate the virtual environment (Windows)
# venv\Scripts\activate

# Install project dependencies
# pip install -r requirements.txt

# Update pip to the latest version
# python -m pip install --upgrade pip
```

## 2. Running the Application
```bash
# Start the FastAPI server with auto-reload (Development)
# uvicorn app.main:app --reload

# Start the server on a specific host and port
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start the server in production mode (No reload)
# uvicorn app.main:app --host 0.0.0.0 --port 8000

# Force stop the server if port 8000 is already in use
# fuser -k 8000/tcp
```

## 3. Database Management (Alembic)
```bash
# Create a new migration revision based on model changes
# alembic revision --autogenerate -m "description_of_changes"

# Create a manual (empty) migration revision
# alembic revision -m "description_of_changes"

# Upgrade the database to the latest version
# alembic upgrade head

# Downgrade the database by one version
# alembic downgrade -1

# View the migration history
# alembic history --verbose

# Check the current migration version of the database
# alembic current
```

## 4. Testing & Verification
```bash
# Run all tests (Pytest)
# pytest -v

# Run the Request Control (Idempotency & Rate Limit) verification script
# python3 scratch/test_request_control.py

# Clear all rate limit records from the database (Useful for resetting tests)
# python3 -c "from app.core.database import SessionLocal; from app.apps.request_control.models import RateLimitRecord; db=SessionLocal(); db.query(RateLimitRecord).delete(); db.commit(); print('Rate limits cleared!')"

# Run a specific test file
# pytest tests/test_filename.py
```

## 5. Logging & Monitoring
```bash
# View live application logs (General traffic)
# tail -f logs/app-$(date +%Y-%m-%d).log

# View live error logs (Database and system crashes)
# tail -f logs/errors.log

# Check the size of log files
# ls -lh logs/
```

## 6. Maintenance & Utilities
```bash
# Clean up Python cache files (__pycache__)
# find . -type d -name "__pycache__" -exec rm -rf {} +

# Export current dependencies to requirements.txt
# pip freeze > requirements.txt

# Check for security vulnerabilities in dependencies
# safety check
```

## 7. Git Workflow (Common)
```bash
# Check status
# git status

# Add all changes
# git add .

# Commit changes
# git commit -m "Your commit message"

# Push to origin
# git push origin main
```

## 8. Background Tasks (Celery & Redis)
```bash
# Start Redis Server (Ensure Redis is installed on your system)
# redis-server

# Start Celery Worker (Run this in a separate terminal)
# celery -A app.core.celery_app worker --loglevel=info

# Monitor Celery Tasks (requires 'flower' package)
# celery -A app.core.celery_app flower
```
