from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.account.models import Account
from app.auth.dependencies import get_current_account
from app.core.exceptions import EventNotFoundError
from app.events.dependencies import get_event_service
from app.events.models import Event
from app.events.schemas import (
    EventCreate,
    EventListResponse,
    EventResponse,
    EventUpdate,
)
from app.events.service import EventService

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


def get_event_or_404(
    event_id: UUID,
    current_account: Account,
    service: EventService,
) -> Event:
    event = service.get(event_id)

    if event.organization_id != current_account.organization_id:
        raise EventNotFoundError()

    return event


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    data: EventCreate,
    current_account: Account = Depends(get_current_account),
    service: EventService = Depends(get_event_service),
):
    return service.create(
        current_account,
        data,
    )


@router.get(
    "",
    response_model=EventListResponse,
)
def list_events(
    current_account: Account = Depends(get_current_account),
    service: EventService = Depends(get_event_service),
):
    return {
        "events": service.list(current_account),
    }


@router.get(
    "/{event_id}",
    response_model=EventResponse,
)
def get_event(
    event_id: UUID,
    current_account: Account = Depends(get_current_account),
    service: EventService = Depends(get_event_service),
):
    event = get_event_or_404(
        event_id,
        current_account,
        service,
    )

    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
)
def update_event(
    event_id: UUID,
    data: EventUpdate,
    current_account: Account = Depends(get_current_account),
    service: EventService = Depends(get_event_service),
):
    event = get_event_or_404(
        event_id,
        current_account,
        service,
    )

    return service.update(
        event,
        data,
    )


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    event_id: UUID,
    current_account: Account = Depends(get_current_account),
    service: EventService = Depends(get_event_service),
):
    event = get_event_or_404(
        event_id,
        current_account,
        service,
    )

    service.delete(event)