from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.events.repository import EventRepository
from app.gallery.repository import GalleryRepository
from app.gallery.service import GalleryService


def get_gallery_service(
    db: Session = Depends(get_db),
) -> GalleryService:
    gallery_repository = GalleryRepository(db)
    event_repository = EventRepository(db)

    return GalleryService(
        gallery_repository,
        event_repository,
    )