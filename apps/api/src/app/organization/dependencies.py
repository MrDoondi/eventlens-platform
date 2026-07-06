from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.organization.repository import OrganizationRepository
from app.organization.service import OrganizationService


def get_organization_repository(
    db: Session = Depends(get_db),
) -> OrganizationRepository:
    return OrganizationRepository(db)


def get_organization_service(
    repository: OrganizationRepository = Depends(
        get_organization_repository,
    ),
) -> OrganizationService:
    return OrganizationService(repository)