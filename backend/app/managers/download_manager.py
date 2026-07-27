import asyncio
import logging
from collections.abc import Callable

from app.schemas.download import (
    DownloadProgress,
    DownloadResult,
    DownloadStatus,
)
from app.services.download_service import DownloadService

logger = logging.getLogger(__name__)


class DownloadManager:
    def __init__(
        self,
        service_factory: Callable[[], DownloadService],
    ):
        self._service_factory = service_factory

        self._task: asyncio.Task | None = None

        self._status = DownloadStatus.IDLE

        self._progress = DownloadProgress()

        self._result: DownloadResult | None = None

    @property
    def status(self) -> DownloadStatus:
        return self._status

    @property
    def progress(self) -> DownloadProgress:
        return self._progress

    @property
    def result(self) -> DownloadResult | None:
        return self._result

    @property
    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    def start(self):
        if self.is_running:
            raise RuntimeError("Download already running.")

        self._status = DownloadStatus.RUNNING

        self._progress = DownloadProgress()

        self._result = None

        self._task = asyncio.create_task(self._run())

    async def _run(self):

        service = self._service_factory()

        service.progress = self._progress

        try:
            result = await service.download_all()

            self._result = result

            if result.status == "completed":
                self._status = DownloadStatus.COMPLETED
            else:
                self._status = DownloadStatus.BLOCKED

        except Exception:
            logger.exception("Download failed.")

            self._status = DownloadStatus.FAILED

            raise
