from fastapi import APIRouter

from app.auth.api import router as auth_router
from app.organization.api import router as organization_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(organization_router)
api_router.include_router(auth_router)