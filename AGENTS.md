# Backend Engineering — AI Agent Rules (FastAPI)

> **Final Principle**
> "Your responsibility is not to generate code fast. Your responsibility is to generate code that can scale without being rewritten."

## 1. Purpose
This document defines the strict rules every AI agent must follow before generating or modifying any code in this project. 
Failure to follow these rules will result in inconsistent architecture, duplicated logic, and hard-to-maintain code. Your job is not just to generate code, but to preserve system integrity.

---

## 2. Required Understanding Before Coding
Before writing any code, you **MUST**:

### 2.1 Read and Understand the Project Structure
```text
app/
├── main.py
├── core/
├── apps/
└── shared/
```

### 2.2 Identify the Feature (App) Being Modified
- **Never create duplicate features.**
- If a feature exists, extend it instead of recreating it.

### 2.3 Understand the Architecture Flow
**Route** → **Service** → **Repository** → **Database**

Each layer has exactly one responsibility:
- **Route**: HTTP handling (request/response)
- **Service**: Business logic
- **Repository**: Database access

### 2.4 Check for Existing Logic
Before creating models, schemas, services, or repositories, you **MUST**:
- Search the codebase.
- Reuse existing functions where possible.
- **Never duplicate logic.**

---

## 3. Architecture Rules (Non-Negotiable)

### 3.1 Routes (`routes.py`)
- **Must only**: Receive requests, validate input, call the service, and return responses.
- ❌ **Forbidden**: Business logic, database queries.

### 3.2 Services (`service.py`)
- **Must contain**: Business rules, workflows, validations beyond basic schemas.
- ❌ **Forbidden**: Direct database queries, HTTP logic.

### 3.3 Repository (`repository.py`)
- **Must contain**: Database queries only.
- ❌ **Forbidden**: Business logic, validation logic.

### 3.4 Schemas (`schemas.py`)
- **Used for**: Input validation, response formatting (Pydantic models).

### 3.5 Models (`models.py`)
- **Used for**: Defining database structure only (SQLAlchemy models).
- ❌ **Forbidden**: Business logic inside models.

### 3.6 Providers (`providers.py`)
- **Used to**: Create services and inject dependencies.

---

## 4. Code Generation Rules

### 4.1 Feature Structure
Do **NOT** write everything in one file. Each feature **MUST** follow this structure:
```text
models.py
schemas.py
repository.py
service.py
routes.py
providers.py
```

### 4.2 Maintain Feature Isolation
- Code inside one feature (e.g., `users/`) must not leak into another (e.g., `payments/`).
- Cross-feature interaction must be explicit and minimal.

### 4.3 Naming Consistency
Use clear and predictable names:
- `UserService`
- `UserRepository`
- `UserCreateSchema`

### 4.4 Function Design
Keep functions small. Each function should:
- Do exactly one thing.
- Be easy to test.

### 4.5 Output Requirements for AI
When generating code:
- Follow project structure exactly.
- Add comments explaining purpose.
- Keep code readable and minimal.
- Do not overengineer.

---

## 5. Safety & Reliability Rules

### 5.1 Prevent Race Conditions
When writing logic that updates data or depends on existing state, you **MUST**:
- Assume concurrent requests.
- Avoid unsafe *read → modify → write* patterns.
- Prefer atomic operations and database constraints (unique, transactions).

### 5.2 Avoid Duplication
Before writing new code:
- Search for existing implementations.
- Reuse instead of rewriting.

### 5.3 Error Handling
- Do not expose raw exceptions.
- Use controlled error messages.
- **No Silent Failures**: Every failure must be explicit. Return meaningful errors.

---

## 6. Database Rules
### 6.1 Migrations
- Use migrations (Alembic).
- Do **NOT** rely on automatic table creation in production.
- Every schema change must be tracked.

### 6.2 Simple Models
- Keep models simple. No business logic inside models.

---

## 7. What to Do When Adding a Feature
Follow this order strictly:
1. **Check** if the feature already exists.
2. **Create or update** the feature files:
   - `models.py`
   - `schemas.py`
   - `repository.py`
   - `service.py`
   - `routes.py`
   - `providers.py`
3. **Register** routes in `main.py`.
4. **Ensure** no duplication.
5. **Ensure** correct layer separation.

---

## 8. Red Flags (Do NOT Do These)
- ❌ Business logic inside routes
- ❌ Database queries inside services
- ❌ Duplicate models or schemas
- ❌ Creating new features when one already exists
- ❌ Writing large unstructured functions
- ❌ Ignoring existing project patterns