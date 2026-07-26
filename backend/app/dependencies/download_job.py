from functools import lru_cache

from app.dependencies.download import (
    get_download_service,
)
from app.jobs.download_job import DownloadJob
from fastapi import Depends


@lru_cache
def get_download_job(
    service=Depends(get_download_service),
):
    return DownloadJob(service)
