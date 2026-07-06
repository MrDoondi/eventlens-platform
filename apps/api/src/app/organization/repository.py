from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.organization.models import Organization
from app.organization.schemas import OrganizationCreate, OrganizationUpdate


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: OrganizationCreate) -> Organization:
        organization = Organization(**data.model_dump())

        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def get_by_id(self, organization_id: UUID) -> Organization | None:
        stmt = select(Organization).where(
            Organization.id == organization_id
        )

        return self.db.scalar(stmt)

    def get_by_slug(self, slug: str) -> Organization | None:
        stmt = select(Organization).where(
            Organization.slug == slug
        )

        return self.db.scalar(stmt)

    def list(self) -> list[Organization]:
        stmt = select(Organization).order_by(
            Organization.created_at.desc()
        )

        return list(self.db.scalars(stmt).all())

    def update(
        self,
        organization: Organization,
        data: OrganizationUpdate,
    ) -> Organization:

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(organization, field, value)

        self.db.commit()
        self.db.refresh(organization)

        return organization

    def delete(self, organization: Organization) -> None:
        self.db.delete(organization)
        self.db.commit()