from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class FileStatistics(Base):
    __tablename__ = "file_statistics"

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"),
        primary_key=True,
    )

    counts: Mapped[dict[str, int]] = mapped_column(
        JSON,
        nullable=False,
    )

    file = relationship(
        "File",
        lazy="joined",
    )
