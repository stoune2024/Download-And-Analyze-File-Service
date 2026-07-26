from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.core.logging import get_logger
from app.integrations.external_api.client import (
    ExternalApiBlockedException,
    ExternalApiClient,
)
from app.models.file import File
from app.schemas.download import DownloadProgress, DownloadResult
from app.storages.archive import ZipExtractor
from app.storages.file_storage import FileStorage
from app.unit_of_work.uow import UnitOfWork

logger = get_logger(__name__)


class DownloadService:
    def __init__(
        self,
        client: ExternalApiClient,
        storage: FileStorage,
        extractor: ZipExtractor,
        uow: UnitOfWork,
    ):

        self.client = client

        self.storage = storage

        self.extractor = extractor

        self.uow = uow

        self.progress = DownloadProgress(
            started_at=datetime.now(ZoneInfo("Asia/Novosibirsk"))
        )

    async def download_all(self) -> DownloadResult:

        try:
            while True:
                names = await self.client.get_names()

                if not names:
                    break

                self.progress.received_names += len(names)

                logger.info(
                    "Progress: received=%d, current_batch=%d, downloaded=%d",
                    self.progress.received_names,
                    self.progress.current_batch_size,
                    self.progress.total_downloaded,
                )

                for chunk in self._chunks(names, 3):
                    archive = await self.client.download(chunk)

                    files = self.extractor.extract(archive)

                    await self._save_files(files)

                    await self.client.mark_downloaded(chunk)

                    self.progress.current_batch_size = len(chunk)
                    self.progress.total_downloaded += len(chunk)

                    logger.info(
                        "Progress: received=%d, current_batch=%d, downloaded=%d",
                        self.progress.received_names,
                        self.progress.current_batch_size,
                        self.progress.total_downloaded,
                    )

            logger.info(
                "Progress: received=%d, current_batch=%d, downloaded=%d",
                self.progress.received_names,
                self.progress.current_batch_size,
                self.progress.total_downloaded,
            )

            return DownloadResult(
                status="completed",
                downloaded=self.progress.total_downloaded,
            )

        except ExternalApiBlockedException as exc:
            logger.warning(
                "External API blocked. Downloaded=%d Retry-After=%s",
                self.progress.total_downloaded,
                exc.retry_after,
            )

            return DownloadResult(
                status="blocked",
                downloaded=self.progress.total_downloaded,
                retry_after=exc.retry_after,
            )

    async def _save_files(
        self,
        files: dict[str, bytes],
    ):

        async with self.uow:
            for filename, content in files.items():
                existing = await self.uow._files.get_by_name(filename)

                if existing:
                    continue

                path = await self.storage.save(
                    filename,
                    content,
                )

                entity = File(
                    name=filename,
                    path=path,
                    downloaded_at=datetime.now(timezone.utc),
                )

                await self.uow._files.add(entity)

    @staticmethod
    def _chunks(
        items: list[str],
        size: int,
    ):

        for i in range(
            0,
            len(items),
            size,
        ):
            yield items[i : i + size]
