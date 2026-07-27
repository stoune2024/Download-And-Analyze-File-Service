from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.download_manager import get_download_manager
from app.managers.download_manager import DownloadManager
from sse_starlette.sse import EventSourceResponse

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


@router.get("/download/events")
async def events(
    manager: DownloadManager = Depends(
        get_download_manager
    ),
):

    async def stream():

        async for event in manager.events():

            yield {
                "event": event.type.value,
                "data": event.model_dump_json(),
            }

    return EventSourceResponse(stream())