from app.core.database import Database
from app.core.logging import get_logger
from app.repositories.file_repository import FileRepository

logger = get_logger(__name__)


class UnitOfWork:
    def __init__(self, database: Database):
        self._database = database

        self._session = None

        self._files = None

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
