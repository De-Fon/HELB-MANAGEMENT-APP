from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


class AppException(Exception):
    """Base exception for all application errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, message=message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=400, message=message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=401, message=message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=403, message=message)


# Global Exception Handler
async def app_exception_handler(request: Request, exc: AppException):
    # 5xx errors are bugs — log as ERROR with full traceback context
    if exc.status_code >= 500:
        logger.error(
            f"[{exc.status_code}] {request.method} {request.url.path} — {exc.message}"
        )
    else:
        # 4xx are expected client errors — log as WARNING (no traceback needed)
        logger.warning(
            f"[{exc.status_code}] {request.method} {request.url.path} — {exc.message}"
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.message},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for any unhandled exceptions — logs full traceback to errors.log."""
    logger.exception(
        f"[500] UNHANDLED {request.method} {request.url.path} — {exc}"
    )
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal server error"},
    )


def setup_exception_handlers(app):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
