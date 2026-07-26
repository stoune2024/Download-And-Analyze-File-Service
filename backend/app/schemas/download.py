from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class DownloadProgress(BaseModel):
    started_at: datetime
    received_names: int = 0

    current_batch_size: int = 0

    total_downloaded: int = 0


class DownloadResult(BaseModel):
    status: Literal["completed", "blocked"]

    downloaded: int

    retry_after: int | None = None
