# Logging System (Loguru Implementation)

The HELB Backend now features a robust, asynchronous logging system powered by **Loguru**. This system is designed to provide maximum visibility into system behavior while maintaining high performance.

## 1. Where are the Logs?

All logs are stored in the `/logs` directory at the root of the project:

- **`logs/app-YYYY-MM-DD.log`**: The daily rotating general log. Contains every request, response, and info-level event.
- **`logs/errors.log`**: A dedicated error log. Contains only `ERROR` and `CRITICAL` events with full stack traces. Kept for 7 days.

## 2. Automated Logging Features

You don't need to manually log basic events; the following are captured automatically:

### HTTP Request/Response Middleware
Every single HTTP request is logged with its method, path, client IP, status code, and processing time.
- **Level**: `INFO` for 2xx/3xx, `WARNING` for 4xx, `ERROR` for 5xx.
- **Implementation**: See `app/shared/middleware.py`.

### Database Error Tracking
Any SQLAlchemy or Database connection error is automatically captured and logged to the `errors.log` file.
- **Implementation**: See `app/core/database.py`.

### Global Exception Handlers
Any exception that escapes a route is caught, returned as a JSON response to the client, and logged with its context.
- **Implementation**: See `app/shared/exceptions.py`.

## 3. How to Log Manually in Features

If you want to log specific events inside your services or repositories, simply import the logger:

```python
from loguru import logger

def my_service_function():
    logger.info("Processing something important...")
    
    if something_is_wrong:
        logger.warning("Something looks suspicious")
        
    try:
        # logic
    except Exception as e:
        logger.error(f"Critical failure: {e}")
```

## 4. Configuration Details

- **Daily Rotation**: `app-*.log` rotates every day at midnight.
- **Size Rotation**: `errors.log` rotates if it reaches 100MB.
- **Retention**: General logs are kept for 30 days; Error logs for 7 days.
- **Compression**: Old logs are automatically zipped to save space.
- **Thread-Safe**: Uses `enqueue=True` for safe logging from multiple threads/async tasks.

## 5. Console Output

In the terminal where you run `uvicorn`, you will see beautiful, colored logs:
- **Green**: Timestamps
- **Cyan**: File, Function, and Line number
- **Level Colors**: Info (White), Warning (Yellow), Error (Red)
