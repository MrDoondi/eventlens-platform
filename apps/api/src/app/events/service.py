from uuid import UUID

from app.account.models import Account
from app.core.exceptions import EventAlreadyExistsError, EventNotFoundError
from app.events.models import Event
from app.events.repository import EventRepository
from app.events.schemas import EventCreate, EventUpdate


class EventService:
    def __init__(
        self,
        repository: EventRepository,
    ):
        self.repository = repository

    def create(
        self,
        current_account: Account,
        data: EventCreate,
    ) -> Event:
        existing = self.repository.get_by_slug(
            current_account.organization_id,
            data.slug,
        )

        if existing:
            raise EventAlreadyExistsError(data.slug)

        if data.end_date < data.start_date:
            raise InvalidEventDatesError()

        return self.repository.create(
            current_account.organization_id,
            data,
        )

    def get(
        self,
        event_id: UUID,
    ) -> Event:
        event = self.repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError()

        return event

    def list(
        self,
        current_account: Account,
    ) -> list[Event]:
        return self.repository.list_by_organization(
            current_account.organization_id,
        )

    def update(
        self,
        event: Event,
        data: EventUpdate,
    ) -> Event:
        if (
            data.start_date
            and data.end_date
            and data.end_date < data.start_date
        ):
            raise InvalidEventDatesError()

        return self.repository.update(
            event,
            data,
        )

    def delete(
        self,
        event: Event,
    ) -> None:
        self.repository.delete(event)