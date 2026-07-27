from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from app.dependencies.file import (
    get_file_service,
)
from app.schemas.file import (
    FilePage,
)
from app.services.file_service import (
    FileService,
)

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


@router.get(
    "",
    response_model=FilePage,
)
async def get_files(
    page: int = Query(1, ge=1),
    size: int = Query(
        20,
        ge=1,
        le=100,
    ),
    service: FileService = Depends(
        get_file_service,
    ),
):

    return await service.get_page(
        page,
        size,
    )
