from collections import Counter

from app.models.file_statistics import FileStatistics as FileStatisticsModel
from app.schemas.statistics import (
    DigitStatistics,
    FileStatistics,
    StatisticsResponse,
)
from app.storages.file_storage import FileStorage
from app.unit_of_work.uow import UnitOfWork


class StatisticsService:
    def __init__(
        self,
        storage: FileStorage,
        uow: UnitOfWork,
    ):
        self.storage = storage
        self.uow = uow

    async def calculate(
        self,
        file_ids: list[int],
    ) -> StatisticsResponse:

        total_counter = Counter()

        per_file: list[FileStatistics] = []

        async with self.uow:
            for file_id in file_ids:
                file = await self.uow.files.get(file_id)

                if file is None:
                    continue

                cached = await self.uow.file_statistics.get(file.id)

                if cached is not None:
                    stats = cached.counts

                else:
                    content = await self.storage.read(file.path)

                    counter = Counter(content)

                    stats = {
                        str(i): counter.get(
                            str(i),
                            0,
                        )
                        for i in range(10)
                    }

                    await self.uow.file_statistics.add(
                        FileStatisticsModel(
                            file_id=file.id,
                            counts=stats,
                        )
                    )

                total_counter.update(stats)

                per_file.append(
                    FileStatistics(
                        id=file.id,
                        name=file.name,
                        statistics=DigitStatistics(
                            counts=stats,
                        ),
                    )
                )

        return StatisticsResponse(
            total=DigitStatistics(
                counts={
                    str(i): total_counter.get(
                        str(i),
                        0,
                    )
                    for i in range(10)
                }
            ),
            files=per_file,
        )
