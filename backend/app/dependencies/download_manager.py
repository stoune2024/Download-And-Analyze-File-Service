from functools import lru_cache

from app.factories.download_service_factory import (
    create_download_service,
)
from app.managers.download_manager import DownloadManager


@lru_cache
def get_download_manager() -> DownloadManager:
    return DownloadManager(
        service_factory=create_download_service,
    )
