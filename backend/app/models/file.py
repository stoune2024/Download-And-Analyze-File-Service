from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    downloaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
