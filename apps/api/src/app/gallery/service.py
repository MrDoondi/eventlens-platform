from uuid import UUID

from app.account.models import Account
from app.core.exceptions import (
    EventNotFoundError,
    GalleryAlreadyExistsError,
    GalleryNotFoundError,
)
from app.events.repository import EventRepository
from app.gallery.models import Gallery
from app.gallery.repository import GalleryRepository
from app.gallery.schemas import GalleryCreate, GalleryUpdate


class GalleryService:
    def __init__(
        self,
        gallery_repository: GalleryRepository,
        event_repository: EventRepository,
    ):
        self.gallery_repository = gallery_repository
        self.event_repository = event_repository

    def create(
        self,
        event_id: UUID,
        current_account: Account,
        data: GalleryCreate,
    ) -> Gallery:
        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError()

        if event.organization_id != current_account.organization_id:
            raise EventNotFoundError()

        existing = self.gallery_repository.get_by_slug(
            event_id,
            data.slug,
        )

        if existing:
            raise GalleryAlreadyExistsError(data.slug)

        return self.gallery_repository.create(
            event_id,
            data,
        )

    def get(
        self,
        gallery_id: UUID,
    ) -> Gallery:
        gallery = self.gallery_repository.get_by_id(gallery_id)

        if gallery is None:
            raise GalleryNotFoundError()

        return gallery

    def list(
        self,
        event_id: UUID,
        current_account: Account,
    ) -> list[Gallery]:
        event = self.event_repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError()

        if event.organization_id != current_account.organization_id:
            raise EventNotFoundError()

        return self.gallery_repository.list_by_event(
            event_id,
        )

    def update(
        self,
        gallery: Gallery,
        data: GalleryUpdate,
    ) -> Gallery:
        return self.gallery_repository.update(
            gallery,
            data,
        )

    def delete(
        self,
        gallery: Gallery,
    ) -> None:
        self.gallery_repository.delete(gallery)