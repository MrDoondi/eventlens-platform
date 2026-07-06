from app.storage.local import LocalStorageService


def get_storage_service():
    """
    Later this will choose between:
        LocalStorageService
        MinIOStorageService
        S3StorageService
    """

    return LocalStorageService()