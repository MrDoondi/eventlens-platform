from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.organization.models import Organization
from app.organization.schemas import (
    OrganizationCreate,
    OrganizationUpdate,
)


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: Session):
        super().__init__(db, Organization)

    def create(
        self,
        data: OrganizationCreate,
    ) -> Organization:
        organization = Organization(
            **data.model_dump(),
        )

        return super().create(organization)

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        statement = (
            select(Organization)
            .where(
                Organization.slug == slug,
            )
        )

        return self.db.scalar(statement)

    def list(self) -> list[Organization]:
        statement = (
            select(Organization)
            .order_by(Organization.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        organization: Organization,
        data: OrganizationUpdate,
    ) -> Organization:
        for key, value in data.model_dump(
            exclude_unset=True,
        ).items():
            setattr(organization, key, value)

        return super().update(organization)