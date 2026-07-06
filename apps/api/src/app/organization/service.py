from uuid import UUID

from app.core.exceptions import OrganizationAlreadyExistsError
from app.organization.repository import OrganizationRepository
from app.organization.schemas import (
    OrganizationCreate,
    OrganizationUpdate,
)
from app.organization.models import Organization


class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    def create(
        self,
        data: OrganizationCreate,
    ) -> Organization:

        existing = self.repository.get_by_slug(data.slug)

        if existing:
            raise OrganizationAlreadyExistsError(
                f"Organization '{data.slug}' already exists."
            )

        return self.repository.create(data)

    def get(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        return self.repository.get_by_id(organization_id)

    def list(self) -> list[Organization]:
        return self.repository.list()

    def update(
        self,
        organization: Organization,
        data: OrganizationUpdate,
    ) -> Organization:
        return self.repository.update(
            organization,
            data,
        )

    def delete(
        self,
        organization: Organization,
    ) -> None:
        self.repository.delete(organization)