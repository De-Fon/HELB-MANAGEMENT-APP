# Request Control Module

The `request_control` module provides essential infrastructure for managing incoming requests, focusing on **Idempotency** and **Rate Limiting**. This module is designed to protect the system from duplicate operations and prevent abuse or accidental flooding of endpoints.

## 1. Features

### Idempotency
Ensures that an operation can be repeated multiple times without changing the result beyond the initial application. This is critical for financial transactions (e.g., loan requests, withdrawals) where network issues might cause a client to retry a request.

*   **Mechanism**: Uses a unique `Idempotency-Key` provided in the request headers.
*   **Storage**: Successful responses are cached in the database with a configurable TTL (default 24 hours).
*   **Behavior**: If a request is received with a key that has already been successfully processed, the module returns the cached response instead of re-executing the logic.

### Rate Limiting
Controls the frequency of requests to specific endpoints to ensure fair usage and protect against Denial of Service (DoS) attacks.

*   **Mechanism**: Implements a sliding window algorithm (database-backed).
*   **Atomicity**: Uses atomic SQL increments (`request_count = request_count + 1`) to ensure correctness under high concurrent load.
*   **Response**: Returns HTTP 429 (Too Many Requests) with a `Retry-After` header when limits are exceeded.

---

## 2. Usage

### Decorators
The module provides two main decorators in `app.apps.request_control.dependencies`:

#### `@idempotent(header_key="Idempotency-Key")`
Apply this to POST endpoints that perform state-changing operations.
*   **Requirement**: The route handler must accept `request: Request`, `db: Session`, and `service: RequestControlService`.

```python
@router.post("/process")
@idempotent()
def process_data(request: Request, db: Session = Depends(get_db), service: RequestControlService = Depends(get_request_control_service)):
    return {"message": "Success"}
```

#### `@rate_limit(max_requests=10, window_seconds=60)`
Apply this to any endpoint to restrict usage.
*   **Requirement**: Same as `@idempotent`.

```python
@router.get("/data")
@rate_limit(max_requests=30, window_seconds=60)
def get_data(request: Request, db: Session = Depends(get_db), service: RequestControlService = Depends(get_request_control_service)):
    return {"data": "..."}
```

---

## 3. Architecture

Following the project's strict **Route → Service → Repository** pattern:

1.  **Repository (`repository.py`)**: Handles all SQL operations, including atomic increments for rate limits and fetching/storing idempotency records.
2.  **Service (`service.py`)**: Orchestrates the logic. Generates endpoint identifiers, validates windows, and manages response caching.
3.  **Dependencies (`dependencies.py`)**: Contains the decorator logic that extracts HTTP headers and manages the flow between the route and the service.

---

## 4. Technical Details

### Concurrency Handling
Unlike standard "read-then-write" patterns, the rate limiter uses an **Atomic Increment** strategy:
```sql
UPDATE rate_limit_records 
SET request_count = request_count + 1 
WHERE id = :record_id
```
This prevents the "Lost Update" problem where multiple simultaneous requests might only increment the count once.

### Endpoint Identification
Endpoints are identified by a combination of `METHOD + PATH` (e.g., `POST /api/v1/auth/login`). This ensures that rate limits and idempotency keys are scoped correctly and don't clash across different features.

---

## 5. Global Configuration (Current Standards)

*   **POST Endpoints**: 5 requests / 60 seconds (with Idempotency).
*   **GET Endpoints**: 30 requests / 60 seconds.
*   **Auth Register**: 3 requests / 300 seconds.
*   **Auth Login**: 10 requests / 300 seconds.
