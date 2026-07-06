from abc import ABC, abstractmethod

from fastapi import UploadFile


class StorageService(ABC):
    @abstractmethod
    async def save(
        self,
        file: UploadFile,
        destination: str,
    ) -> str:
        """
        Save a file and return the storage key.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        storage_key: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        storage_key: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_url(
        self,
        storage_key: str,
    ) -> str:
        raise NotImplementedError