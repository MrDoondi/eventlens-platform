from pathlib import Path
import shutil

from fastapi import UploadFile

from app.storage.base import StorageService


UPLOAD_ROOT = Path("uploads")


class LocalStorageService(StorageService):

    async def save(
        self,
        file: UploadFile,
        destination: str,
    ) -> str:

        file_path = UPLOAD_ROOT / destination

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return destination

    async def delete(
        self,
        storage_key: str,
    ) -> None:

        path = UPLOAD_ROOT / storage_key

        if path.exists():
            path.unlink()

    def exists(
        self,
        storage_key: str,
    ) -> bool:

        return (UPLOAD_ROOT / storage_key).exists()

    def get_url(
        self,
        storage_key: str,
    ) -> str:

        return f"/uploads/{storage_key}"