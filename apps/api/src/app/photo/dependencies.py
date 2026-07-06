from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.gallery.repository import GalleryRepository
from app.photo.repository import PhotoRepository
from app.photo.service import PhotoService
from app.storage.factory import get_storage_service


def get_photo_service(
    db: Session = Depends(get_db),
):
    return PhotoService(
        repository=PhotoRepository(db),
        gallery_repository=GalleryRepository(db),
        storage=get_storage_service(),
    )