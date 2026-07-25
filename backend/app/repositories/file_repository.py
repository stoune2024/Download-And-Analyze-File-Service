from sqlalchemy import select

from app.models.file import File
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository):
    async def add(self, file: File) -> None:
        self._session.add(file)

    async def get_by_name(self, name: str) -> File | None:
        stmt = select(File).where(File.name == name)

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()
