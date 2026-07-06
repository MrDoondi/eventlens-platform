from fastapi import APIRouter

from app.organization.api import router as organization_router

api_router = APIRouter()

api_router.include_router(
    organization_router,
)