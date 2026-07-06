from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    print("🚀 EventLens API starting...")

    yield

    print("🛑 EventLens API shutting down...")