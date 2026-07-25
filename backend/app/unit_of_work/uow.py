from app.core.database import Database
from app.repositories.file_repository import FileRepository


class UnitOfWork:
    def __init__(self, database: Database):
        self._database = database

        self._session = None

        self._files = None

    @property
    def files(self) -> FileRepository:

        if self._files is None:
            self._files = FileRepository(self._session)

        return self._files

    @property
    def statistics(self): ...

    @property
    def downloads(self): ...

    @property
    def cache(self): ...

    async def __aenter__(self):

        self._session = self._database.get_session()

        return self

    async def __aexit__(self, exc_type, exc, tb):

        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()

        await self._session.close()
