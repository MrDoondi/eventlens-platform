from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import EventStatus, EventType


class EventCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    slug: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    event_type: EventType

    venue: str | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    timezone: str = "UTC"

    start_date: datetime

    end_date: datetime

    cover_image: str | None = None

    is_public: bool = False


class EventUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    venue: str | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    timezone: str | None = None

    start_date: datetime | None = None

    end_date: datetime | None = None

    cover_image: str | None = None

    status: EventStatus | None = None

    is_public: bool | None = None


class EventResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    organization_id: UUID

    title: str

    slug: str

    description: str | None

    event_type: EventType

    venue: str | None

    city: str | None

    state: str | None

    country: str | None

    timezone: str

    start_date: datetime

    end_date: datetime

    cover_image: str | None

    status: EventStatus

    is_public: bool

    created_at: datetime

    updated_at: datetime


class EventListResponse(BaseModel):
    events: list[EventResponse]