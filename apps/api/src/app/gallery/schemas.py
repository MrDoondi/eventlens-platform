from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GalleryCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    slug: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    cover_image: str | None = None

    sort_order: int = 0

    is_public: bool = False


class GalleryUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    cover_image: str | None = None

    sort_order: int | None = None

    is_public: bool | None = None


class GalleryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    event_id: UUID

    title: str

    slug: str

    description: str | None

    cover_image: str | None

    sort_order: int

    is_public: bool

    created_at: datetime

    updated_at: datetime


class GalleryListResponse(BaseModel):
    galleries: list[GalleryResponse]