from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.core.enums import PhotoStatus


class PhotoResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    gallery_id: UUID

    uploaded_by: UUID | None

    filename: str

    original_filename: str

    storage_key: str

    thumbnail_key: str | None

    mime_type: str

    file_size: int

    width: int | None

    height: int | None

    status: PhotoStatus

    created_at: datetime

    updated_at: datetime


class PhotoListResponse(BaseModel):
    photos: list[PhotoResponse]