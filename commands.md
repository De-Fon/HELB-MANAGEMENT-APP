# Project Commands Reference

This file contains every command you might need to run for this project, categorised and commented out for safe reference.

## 1. Environment & Setup
```bash
# Create a virtual environment
# python -m venv venv
# python3 -m venv venv

# Activate the virtual environment (Linux/macOS)
# source venv/bin/activate

# Activate the virtual environment (Windows)
# venv\Scripts\activate

# Install project dependencies
# pip install -r requirements.txt
# ./venv/bin/pip install -r requirements.txt

# Update pip to the latest version
# python -m pip install --upgrade pip
# ./venv/bin/python -m pip install --upgrade pip
```

## 2. Running the Application
```bash
# Start the FastAPI server with auto-reload (Development)
# uvicorn app.main:app --reload
# ./venv/bin/uvicorn app.main:app --reload

# Start the server on a specific host and port
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start the server in production mode (No reload)
# uvicorn app.main:app --host 0.0.0.0 --port 8000
# ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

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
# ./venv/bin/alembic upgrade head

# Downgrade the database by one version
# alembic downgrade -1
# ./venv/bin/alembic downgrade -1

# View the migration history
# alembic history --verbose
# ./venv/bin/alembic history --verbose

# Check the current migration version of the database
# alembic current
# ./venv/bin/alembic current
```

## 4. Testing & Verification
```bash
# Run all tests (Pytest)
# pytest -v
# ./venv/bin/python -m pytest -v

# Run the Request Control / Idempotency verification script
# python3 scratch/test_request_control.py
# ./venv/bin/python scratch/test_request_control.py

# Compile the app and catch syntax/import issues quickly
# ./venv/bin/python -m compileall app

# Collect tests without running them
# ./venv/bin/python -m pytest --collect-only -q

# Run a specific test file
# pytest tests/test_filename.py
# ./venv/bin/python -m pytest tests/test_budget_tracker.py -v
```

## 5. Redis & SlowAPI Rate Limiting
```bash
# Start Redis manually in the foreground
# redis-server

# Manage Redis as a background service (Recommended for Linux/Ubuntu)
# sudo systemctl status redis-server
# sudo systemctl start redis-server
# sudo systemctl restart redis-server
# sudo systemctl stop redis-server

# Verify Redis is running
# redis-cli ping

# Check Redis DB 1, used by REDIS_RATE_LIMIT_URL=redis://localhost:6379/1
# redis-cli -n 1 DBSIZE
# redis-cli -n 1 KEYS '*'

# Clear only the rate-limiting Redis DB
# redis-cli -n 1 FLUSHDB

# Start the API with Redis-backed rate limiting enabled
# REDIS_RATE_LIMIT_URL=redis://localhost:6379/1 ./venv/bin/uvicorn app.main:app --reload

# Temporarily disable rate limiting for local debugging
# RATE_LIMIT_ENABLED=false ./venv/bin/uvicorn app.main:app --reload

# Use in-memory rate-limit storage for local/sandbox checks
# REDIS_RATE_LIMIT_URL=memory:// ./venv/bin/uvicorn app.main:app --reload

# Quick health check
# curl -i http://127.0.0.1:8000/health

# Quick auth rate-limit check: login allows 10 requests per 5 minutes
# curl -i -X POST http://127.0.0.1:8000/api/v1/auth/login \
#   -H "Content-Type: application/json" \
#   -d '{"email_or_username":"testuser@helb.com","password":"SecurePass123!"}'

# Quick budget tracker rate-limit check: allocate allows 5 requests per minute
# curl -i -X POST http://127.0.0.1:8000/api/v1/budget-tracker/allocate \
#   -H "Content-Type: application/json" \
#   -H "Idempotency-Key: budget-test-1" \
#   -d '{"user_id":1,"total_helb_amount":10000,"categories":{"rent":4000,"food":3000}}'
```

## 6. Logging & Monitoring
```bash
# View live application logs (General traffic)
# tail -f logs/app-$(date +%Y-%m-%d).log

# View live error logs (Database and system crashes)
# tail -f logs/errors.log

# Check the size of log files
# ls -lh logs/
```

## 7. Maintenance & Utilities
```bash
# Clean up Python cache files (__pycache__)
# find . -type d -name "__pycache__" -exec rm -rf {} +

# Export current dependencies to requirements.txt
# pip freeze > requirements.txt

# Check for security vulnerabilities in dependencies
# safety check
```

## 8. Git Workflow (Common)
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

## 9. Background Tasks (Celery & Redis)
```bash
# Start Celery Worker (Run this in a separate terminal)
# celery -A app.core.celery_app worker --loglevel=info
# ./venv/bin/celery -A app.core.celery_app worker --loglevel=info

# Monitor Celery Tasks (requires 'flower' package)
# celery -A app.core.celery_app flower
# ./venv/bin/celery -A app.core.celery_app flower
```
