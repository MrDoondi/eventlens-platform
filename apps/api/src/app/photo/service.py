from pathlib import Path
from uuid import UUID, uuid4

from PIL import Image
from fastapi import UploadFile

from app.account.models import Account
from app.core.config import get_settings
from app.core.enums import PhotoStatus
from app.core.exceptions import GalleryNotFoundError
from app.gallery.repository import GalleryRepository
from app.photo.models import Photo
from app.photo.repository import PhotoRepository
from app.storage.base import StorageService
from app.storage.utils import generate_thumbnail
from app.validators.image import ImageValidator

settings = get_settings()


class PhotoService:
    def __init__(
        self,
        repository: PhotoRepository,
        gallery_repository: GalleryRepository,
        storage: StorageService,
    ):
        self.repository = repository
        self.gallery_repository = gallery_repository
        self.storage = storage

    async def upload(
        self,
        gallery_id: UUID,
        current_account: Account,
        file: UploadFile,
    ) -> Photo:

        # ----------------------------
        # Validate uploaded file
        # ----------------------------
        ImageValidator.validate_content_type(file)

        await ImageValidator.validate_size(
            file,
            settings.MAX_UPLOAD_SIZE,
        )

        await ImageValidator.validate_image(file)

        # ----------------------------
        # Get gallery
        # ----------------------------
        gallery = self.gallery_repository.get_by_id(
            gallery_id,
        )

        if gallery is None:
            raise GalleryNotFoundError()

        # ----------------------------
        # Verify gallery ownership
        # ----------------------------
        if (
            gallery.event.organization_id
            != current_account.organization_id
        ):
            raise GalleryNotFoundError()

        # ----------------------------
        # Generate filename
        # ----------------------------
        extension = Path(
            file.filename,
        ).suffix.lower()

        filename = f"{uuid4()}{extension}"

        storage_key = (
            f"organizations/"
            f"{current_account.organization_id}/"
            f"events/{gallery.event_id}/"
            f"galleries/{gallery.id}/"
            f"originals/{filename}"
        )

        thumbnail_key = (
            f"organizations/"
            f"{current_account.organization_id}/"
            f"events/{gallery.event_id}/"
            f"galleries/{gallery.id}/"
            f"thumbnails/{filename}"
        )

        # ----------------------------
        # Calculate actual file size
        # ----------------------------
        contents = await file.read()

        file_size = len(contents)

        await file.seek(0)

        # ----------------------------
        # Save original image
        # ----------------------------
        await self.storage.save(
            file,
            storage_key,
        )

        try:
            # ----------------------------
            # Generate thumbnail
            # ----------------------------
            generate_thumbnail(
                Path(settings.UPLOAD_DIRECTORY) / storage_key,
                Path(settings.UPLOAD_DIRECTORY) / thumbnail_key,
            )

            # ----------------------------
            # Read image metadata
            # ----------------------------
            with Image.open(
                Path(settings.UPLOAD_DIRECTORY) / storage_key
            ) as image:
                width, height = image.size

            # ----------------------------
            # Save database record
            # ----------------------------
            photo = Photo(
                gallery_id=gallery.id,
                uploaded_by=current_account.id,
                filename=filename,
                original_filename=file.filename,
                storage_key=storage_key,
                thumbnail_key=thumbnail_key,
                mime_type=file.content_type,
                file_size=file_size,
                width=width,
                height=height,
                status=PhotoStatus.UPLOADED,
            )

            return self.repository.create(photo)

        except Exception:
            # Roll back files if database save fails
            await self.storage.delete(storage_key)
            await self.storage.delete(thumbnail_key)
            raise

    def list(
        self,
        gallery_id: UUID,
    ) -> list[Photo]:
        return self.repository.list_by_gallery(
            gallery_id,
        )