from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException, UploadFile, status


ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


class ImageValidator:

    @staticmethod
    def validate_content_type(
        file: UploadFile,
    ) -> None:

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG and WEBP images are allowed.",
            )

    @staticmethod
    async def validate_size(
        file: UploadFile,
        max_size: int,
    ) -> None:

        contents = await file.read()

        size = len(contents)

        await file.seek(0)

        if size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Maximum upload size is {max_size // (1024 * 1024)} MB.",
            )

    @staticmethod
    async def validate_image(
        file: UploadFile,
    ) -> None:

        try:
            image = Image.open(file.file)
            image.verify()

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image.",
            )

        finally:
            await file.seek(0)