from functools import lru_cache

from app.core.database import Database
from app.dependencies.database import (
    get_database,
)
from app.dependencies.external_api import (
    get_external_api_client,
)
from app.integrations.external_api.client import (
    ExternalApiClient,
)
from app.services.download_service import (
    DownloadService,
)
from app.storages.archive import (
    ZipExtractor,
)
from app.storages.file_storage import (
    FileStorage,
)
from app.unit_of_work.uow import UnitOfWork
from fastapi import Depends


@lru_cache
def get_storage():

    return FileStorage("storage/files")


def get_download_service(
    client: ExternalApiClient = Depends(get_external_api_client),
    database: Database = Depends(get_database),
):

    return DownloadService(
        client=client,
        storage=get_storage(),
        extractor=ZipExtractor(),
        uow=UnitOfWork(database),
    )
