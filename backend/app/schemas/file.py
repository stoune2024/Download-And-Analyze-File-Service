from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    id: int

    name: str

    path: str

    downloaded_at: datetime

    model_config = {
        "from_attributes": True,
    }


class FilePage(BaseModel):
    items: list[FileResponse]

    page: int

    size: int

    total: int

    pages: int
