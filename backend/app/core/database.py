from app.core.config import Settings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    """Инкапсулирует Engine и фабрику сессий."""

    def __init__(self, settings: Settings):
        self.engine: AsyncEngine = create_async_engine(
            settings.database_url,
            echo=settings.sql_echo,
            future=True,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def get_session(self) -> AsyncSession:
        return self.session_factory()
