from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.organization import get_organization_service
from app.organization.service import OrganizationService
from app.organization.schemas import (
    OrganizationCreate,
    OrganizationListResponse,
    OrganizationResponse,
)
from app.organization.service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


# def get_service(db: Session = Depends(get_db)) -> OrganizationService:
#     repository = OrganizationRepository(db)
#     return OrganizationService(repository)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    data: OrganizationCreate,
    service: OrganizationService = Depends(get_organization_service),
):
    return service.create(data)


@router.get(
    "",
    response_model=OrganizationListResponse,
)
def list_organizations(
    service: OrganizationService = Depends(get_organization_service),
):
    return {
        "organizations": service.list(),
    }


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    organization = service.get(organization_id)

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    return organization