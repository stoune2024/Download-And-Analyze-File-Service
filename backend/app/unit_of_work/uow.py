from app.core.database import Database
from app.repositories.file_repository import FileRepository


class UnitOfWork:

    def __init__(self, database: Database):
        self._database = database

    async def __aenter__(self):
        self.session = self._database.session()

        self.files = FileRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()