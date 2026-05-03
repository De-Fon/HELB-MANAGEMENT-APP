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

# Run the server in production mode (No reload)
# uvicorn app.main:app --host 0.0.0.0 --port 8000
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

## 4. Testing (Pytest)
```bash
# Run all tests
# pytest

# Run tests with verbose output
# pytest -v

# Run tests and show print statements (no capture)
# pytest -s

# Run a specific test file
# pytest tests/test_filename.py

# Run tests matching a specific keyword
# pytest -k "keyword"

# Run tests and stop immediately on first failure
# pytest -x
```

## 5. Maintenance & Utilities
```bash
# Clean up Python cache files (__pycache__)
# find . -type d -name "__pycache__" -exec rm -rf {} +

# Export current dependencies to requirements.txt
# pip freeze > requirements.txt

# Check for security vulnerabilities in dependencies (requires 'safety' package)
# safety check

# Linting and Formatting (if tools like black/ruff are installed)
# black .
# ruff check .
```

## 6. Git Workflow (Common)
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
