from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.photo.models import Photo


class PhotoRepository(BaseRepository[Photo]):
    def __init__(self, db: Session):
        super().__init__(db, Photo)

    def list_by_gallery(
        self,
        gallery_id: UUID,
    ) -> list[Photo]:
        statement = (
            select(Photo)
            .where(
                Photo.gallery_id == gallery_id,
            )
            .order_by(Photo.created_at.desc())
        )

        return list(self.db.scalars(statement).all())