from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.download_manager import get_download_manager
from app.managers.download_manager import DownloadManager

router = APIRouter()


@router.post(
    "/download",
    status_code=202,
)
async def start_download(
    manager: DownloadManager = Depends(get_download_manager),
):

    if manager.is_running:
        raise HTTPException(
            status_code=409,
            detail="Download already running.",
        )

    manager.start()

    return {
        "status": "started",
    }
