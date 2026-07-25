from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import File


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, file: File):
        self.session.add(file)

    async def get(self, file_id: int) -> File | None:
        result = await self.session.execute(select(File).where(File.id == file_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> File | None:
        result = await self.session.execute(select(File).where(File.name == name))
        return result.scalar_one_or_none()

    async def list(self):
        result = await self.session.execute(select(File))
        return result.scalars().all()
