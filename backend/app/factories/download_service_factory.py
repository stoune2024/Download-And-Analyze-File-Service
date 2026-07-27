from functools import lru_cache

from app.dependencies.database import get_database
from app.dependencies.external_api import get_external_api_client
from app.services.download_service import DownloadService
from app.storages.archive import ZipExtractor
from app.storages.file_storage import FileStorage
from app.unit_of_work.uow import UnitOfWork


@lru_cache
def get_storage() -> FileStorage:
    return FileStorage("storage/files")


@lru_cache
def get_zip_extractor() -> ZipExtractor:
    return ZipExtractor()


def create_download_service() -> DownloadService:

    database = get_database()

    client = get_external_api_client()

    return DownloadService(
        client=client,
        storage=get_storage(),
        extractor=get_zip_extractor(),
        uow=UnitOfWork(database),
    )
