from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.events.models import Event
from app.events.schemas import EventCreate, EventUpdate


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        organization_id: UUID,
        data: EventCreate,
    ) -> Event:
        event = Event(
            organization_id=organization_id,
            **data.model_dump(),
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event

    def get_by_id(
        self,
        event_id: UUID,
    ) -> Event | None:
        statement = (
            select(Event)
            .where(Event.id == event_id)
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        organization_id: UUID,
        slug: str,
    ) -> Event | None:
        statement = (
            select(Event)
            .where(
                Event.organization_id == organization_id,
                Event.slug == slug,
            )
        )

        return self.db.scalar(statement)

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Event]:
        statement = (
            select(Event)
            .where(Event.organization_id == organization_id)
            .order_by(Event.start_date.desc())
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        event: Event,
        data: EventUpdate,
    ) -> Event:
        for key, value in data.model_dump(
            exclude_unset=True,
        ).items():
            setattr(event, key, value)

        self.db.commit()
        self.db.refresh(event)

        return event

    def delete(
        self,
        event: Event,
    ) -> None:
        self.db.delete(event)
        self.db.commit()