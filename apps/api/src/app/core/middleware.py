import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = round(time.time() - start, 3)

        logger.info(
            "%s %s %s %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response