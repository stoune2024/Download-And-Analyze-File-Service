from app.core.database import Database
from app.core.logging import get_logger
from app.repositories.file_repository import FileRepository
from app.repositories.file_statistics_repository import FileStatisticsRepository

logger = get_logger(__name__)


class UnitOfWork:
    def __init__(self, database: Database):
        self._database = database

        self._session = None

        self._files = None

        self._file_statistics = None

    async def __aenter__(self):

        self._session = self._database.get_session()

        self._files = FileRepository(self._session)

        return self

    async def __aexit__(self, exc_type, exc, tb):

        logger.info("EXIT", exc_type)

        if exc_type:
            logger.info("ROLLBACK")
            await self._session.rollback()
        else:
            logger.info("COMMIT")
            await self._session.commit()

        await self._session.close()

    @property
    def files(self):
        return self._files

    @property
    def file_statistics(self) -> FileStatisticsRepository:

        if self._file_statistics is None:
            self._file_statistics = FileStatisticsRepository(self._session)

        return self._file_statistics
