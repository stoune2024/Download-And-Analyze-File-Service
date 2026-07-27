from __future__ import annotations

import math

from app.schemas.file import (
    FilePage,
    FileResponse,
)
from app.unit_of_work.uow import UnitOfWork


class FileService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    async def get_page(
        self,
        page: int,
        size: int,
    ) -> FilePage:

        async with self.uow:
            files, total = await self.uow.files.paginate(
                page,
                size,
            )

        return FilePage(
            items=[FileResponse.model_validate(f) for f in files],
            page=page,
            size=size,
            total=total,
            pages=math.ceil(total / size) if total else 1,
        )
