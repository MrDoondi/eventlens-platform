from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import PhotoStatus
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.account.models import Account
    from app.gallery.models import Gallery


class Photo(BaseModel):
    __tablename__ = "photos"

    gallery_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "galleries.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    uploaded_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "accounts.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    thumbnail_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[PhotoStatus] = mapped_column(
        Enum(
            PhotoStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="photo_status",
        ),
        default=PhotoStatus.UPLOADED,
        nullable=False,
    )

    gallery: Mapped["Gallery"] = relationship(
        "Gallery",
        back_populates="photos",
    )

    uploader: Mapped["Account"] = relationship(
        "Account",
    )