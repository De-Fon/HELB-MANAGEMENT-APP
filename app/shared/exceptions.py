from fastapi import Request
from fastapi.responses import JSONResponse

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
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.message},
    )

def setup_exception_handlers(app):
    app.add_exception_handler(AppException, app_exception_handler)
