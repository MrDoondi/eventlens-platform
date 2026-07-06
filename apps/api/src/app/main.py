from fastapi import FastAPI

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Register middleware
    register_middleware(app)

    # Register exception handlers
    register_exception_handlers(app)

    # Health Check Endpoint
    @app.get("/health", tags=["System"])
    async def health():
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }

    return app


app = create_app()