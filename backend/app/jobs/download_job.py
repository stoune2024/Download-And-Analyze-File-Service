import asyncio

from app.services.download_service import DownloadService


class DownloadJob:
    def __init__(
        self,
        service: DownloadService,
    ):

        self._service = service

        self._task: asyncio.Task | None = None

    @property
    def is_running(self) -> bool:

        return self._task is not None and not self._task.done()

    def start(self):

        if self.is_running:
            raise RuntimeError("Download already running.")

        self._task = asyncio.create_task(self._service.download_all())
