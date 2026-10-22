class AppError(Exception):
    status_code = 400
    default_code = "APP_ERROR"

    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.default_code

class UnauthorizedError(AppError):
    status_code = 401
    default_code = "UNAUTHORIZED"

class ForbiddenError(AppError):
    status_code = 403
    default_code = "FORBIDDEN"

class NotFoundError(AppError):
    status_code = 404
    default_code = "NOT_FOUND"

class ConflictError(AppError):
    status_code = 409
    default_code = "CONFLICT"
