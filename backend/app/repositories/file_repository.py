from __future__ import annotations

from sqlalchemy import func, select

from app.models.file import File
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository):
    async def add(self, file: File) -> None:
        self._session.add(file)

    async def get(self, file_id: int) -> File | None:
        stmt = select(File).where(File.id == file_id)

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> File | None:
        stmt = select(File).where(File.name == name)

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def list(self) -> list[File]:
        stmt = select(File).order_by(File.downloaded_at.desc())

        result = await self._session.execute(stmt)

        return list(result.scalars())

    async def paginate(
        self,
        page: int,
        size: int,
    ) -> tuple[list[File], int]:
        total = await self._session.scalar(select(func.count()).select_from(File))

        stmt = (
            select(File)
            .order_by(File.downloaded_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await self._session.execute(stmt)

        return (
            list(result.scalars()),
            total or 0,
        )
