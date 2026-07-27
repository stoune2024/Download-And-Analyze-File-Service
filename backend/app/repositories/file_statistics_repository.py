from sqlalchemy import select

from app.models.file_statistics import FileStatistics
from app.repositories.base import BaseRepository


class FileStatisticsRepository(BaseRepository):
    async def get(
        self,
        file_id: int,
    ) -> FileStatistics | None:

        stmt = select(FileStatistics).where(FileStatistics.file_id == file_id)

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def add(
        self,
        statistics: FileStatistics,
    ) -> None:

        self._session.add(statistics)
