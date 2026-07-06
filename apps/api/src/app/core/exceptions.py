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