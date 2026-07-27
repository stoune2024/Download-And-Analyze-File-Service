from datetime import datetime
from enum import Enum
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel


class DownloadProgress(BaseModel):
    started_at: datetime = datetime.now(ZoneInfo("Asia/Novosibirsk"))
    received_names: int = 0

    current_batch_size: int = 0

    total_downloaded: int = 0


class DownloadResult(BaseModel):
    status: Literal["completed", "blocked"]

    downloaded: int

    retry_after: int | None = None


class DownloadStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class DownloadEventType(str, Enum):
    STARTED = "started"

    RECEIVED_NAMES = "received_names"

    DOWNLOADED = "downloaded"

    FINISHED = "finished"

    BLOCKED = "blocked"

    FAILED = "failed"


class DownloadEvent(BaseModel):
    type: DownloadEventType

    progress: DownloadProgress

    message: str | None = None
