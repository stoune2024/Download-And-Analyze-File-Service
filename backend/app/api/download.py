from fastapi import APIRouter, Depends

from app.dependencies.download import (
    get_download_service,
)
from app.services.download_service import (
    DownloadService,
)

router = APIRouter()


@router.post("/download")
async def download(
    service: DownloadService = Depends(get_download_service),
):

    count = await service.download_all()

    return {"downloaded": count}
