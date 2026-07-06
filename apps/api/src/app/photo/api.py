from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)

from app.account.models import Account
from app.auth.dependencies import get_current_account
from app.photo.dependencies import get_photo_service
from app.photo.schemas import (
    PhotoListResponse,
    PhotoResponse,
)
from app.photo.service import PhotoService

router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)


@router.post(
    "/upload/{gallery_id}",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_photo(
    gallery_id: UUID,
    file: UploadFile = File(...),
    current_account: Account = Depends(
        get_current_account,
    ),
    service: PhotoService = Depends(
        get_photo_service,
    ),
):
    return await service.upload(
        gallery_id,
        current_account,
        file,
    )


@router.get(
    "/gallery/{gallery_id}",
    response_model=PhotoListResponse,
)
def list_photos(
    gallery_id: UUID,
    service: PhotoService = Depends(
        get_photo_service,
    ),
):
    return {
        "photos": service.list(
            gallery_id,
        )
    }