from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class EventLensException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


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
    
class OrganizationAlreadyExistsError(Exception):
    """Raised when an organization slug already exists."""