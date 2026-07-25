from app.core.database import SessionFactory
from app.repositories.file_repository import FileRepository


class UnitOfWork:
    async def __aenter__(self):
        self.session = SessionFactory()

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
