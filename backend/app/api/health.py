from app.unit_of_work.uow import UnitOfWork
from fastapi import APIRouter
from app.dependencies.uow import get_uow
from fastapi import Depends

router = APIRouter(tags=["Health"])


@router.get("/")
async def health():
    return {
        "status": "ok",
        "service": "File Downloader API",
    }


@router.get("/db")
async def db_check(
    uow: UnitOfWork = Depends(get_uow),
):
    async with uow:
        files = await uow.files.list()

    return {"count": len(files)}
