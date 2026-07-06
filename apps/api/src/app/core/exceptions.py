from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class EventLensException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# =========================
# Organization Exceptions
# =========================

class OrganizationAlreadyExistsError(EventLensException):
    def __init__(self, slug: str):
        super().__init__(
            code="organization_already_exists",
            message=f"Organization '{slug}' already exists.",
            status_code=409,
        )


class OrganizationNotFoundError(EventLensException):
    def __init__(self):
        super().__init__(
            code="organization_not_found",
            message="Organization not found.",
            status_code=404,
        )


# =========================
# Account Exceptions
# =========================

class AccountAlreadyExistsError(EventLensException):
    def __init__(self):
        super().__init__(
            code="account_already_exists",
            message="An account with this email already exists.",
            status_code=409,
        )


# =========================
# Authentication Exceptions
# =========================

class InvalidCredentialsError(EventLensException):
    def __init__(self):
        super().__init__(
            code="invalid_credentials",
            message="Invalid email or password.",
            status_code=401,
        )


class AuthenticationError(EventLensException):
    def __init__(self):
        super().__init__(
            code="authentication_failed",
            message="Authentication failed.",
            status_code=401,
        )

class GalleryAlreadyExistsError(EventLensException):
    def __init__(self, slug: str):
        super().__init__(
            code="gallery_already_exists",
            message=f"A gallery with slug '{slug}' already exists.",
            status_code=409,
        )


class GalleryNotFoundError(EventLensException):
    def __init__(self):
        super().__init__(
            code="gallery_not_found",
            message="Gallery not found.",
            status_code=404,
        )

# =========================
# Exception Handler
# =========================

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EventLensException)
    async def eventlens_exception_handler(
        request: Request,
        exc: EventLensException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                },
            },
        )

class EventAlreadyExistsError(EventLensException):
    def __init__(self, slug: str):
        super().__init__(
            code="event_already_exists",
            message=f"An event with slug '{slug}' already exists.",
            status_code=409,
        )


class EventNotFoundError(EventLensException):
    def __init__(self):
        super().__init__(
            code="event_not_found",
            message="Event not found.",
            status_code=404,
        )

class InvalidEventDatesError(EventLensException):
    def __init__(self):
        super().__init__(
            code="invalid_event_dates",
            message="End date cannot be before start date.",
            status_code=400,
        )