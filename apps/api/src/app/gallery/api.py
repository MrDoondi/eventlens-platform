from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.account.models import Account
from app.auth.dependencies import get_current_account
from app.gallery.dependencies import get_gallery_service
from app.gallery.schemas import (
    GalleryCreate,
    GalleryListResponse,
    GalleryResponse,
    GalleryUpdate,
)
from app.gallery.service import GalleryService

router = APIRouter(
    prefix="/galleries",
    tags=["Galleries"],
)


@router.post(
    "/events/{event_id}",
    response_model=GalleryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_gallery(
    event_id: UUID,
    data: GalleryCreate,
    current_account: Account = Depends(get_current_account),
    service: GalleryService = Depends(get_gallery_service),
):
    return service.create(
        event_id,
        current_account,
        data,
    )


@router.get(
    "/events/{event_id}",
    response_model=GalleryListResponse,
)
def list_galleries(
    event_id: UUID,
    current_account: Account = Depends(get_current_account),
    service: GalleryService = Depends(get_gallery_service),
):
    return {
        "galleries": service.list(
            event_id,
            current_account,
        )
    }


@router.get(
    "/{gallery_id}",
    response_model=GalleryResponse,
)
def get_gallery(
    gallery_id: UUID,
    service: GalleryService = Depends(get_gallery_service),
):
    return service.get(gallery_id)


@router.patch(
    "/{gallery_id}",
    response_model=GalleryResponse,
)
def update_gallery(
    gallery_id: UUID,
    data: GalleryUpdate,
    service: GalleryService = Depends(get_gallery_service),
):
    gallery = service.get(gallery_id)

    return service.update(
        gallery,
        data,
    )


@router.delete(
    "/{gallery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_gallery(
    gallery_id: UUID,
    service: GalleryService = Depends(get_gallery_service),
):
    gallery = service.get(gallery_id)

    service.delete(gallery)