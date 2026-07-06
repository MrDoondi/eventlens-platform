from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.gallery.models import Gallery
from app.gallery.schemas import GalleryCreate, GalleryUpdate


class GalleryRepository(BaseRepository[Gallery]):
    def __init__(self, db: Session):
        super().__init__(db, Gallery)

    def create(
        self,
        event_id: UUID,
        data: GalleryCreate,
    ) -> Gallery:
        gallery = Gallery(
            event_id=event_id,
            **data.model_dump(),
        )

        return super().create(gallery)

    def get_by_slug(
        self,
        event_id: UUID,
        slug: str,
    ) -> Gallery | None:
        statement = (
            select(Gallery)
            .where(
                Gallery.event_id == event_id,
                Gallery.slug == slug,
            )
        )

        return self.db.scalar(statement)

    def list_by_event(
        self,
        event_id: UUID,
    ) -> list[Gallery]:
        statement = (
            select(Gallery)
            .where(
                Gallery.event_id == event_id,
            )
            .order_by(Gallery.sort_order)
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        gallery: Gallery,
        data: GalleryUpdate,
    ) -> Gallery:
        for key, value in data.model_dump(
            exclude_unset=True,
        ).items():
            setattr(gallery, key, value)

        return super().update(gallery)