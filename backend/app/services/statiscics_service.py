from collections import Counter

from app.cache.statistics_cache import StatisticsCache
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
        cache: StatisticsCache,
        uow: UnitOfWork,
    ):
        self.storage = storage
        self.cache = cache
        self.uow = uow

    async def calculate(
        self,
        file_ids: list[int],
    ) -> StatisticsResponse:
        async with self.uow:
            files = []

            for file_id in file_ids:
                file = await self.uow.files.get(file_id)

                if file:
                    files.append(file)

        total_counter = Counter()

        per_file = []

        for file in files:
            cached = self.cache.get(file.id)

            if cached:
                stats = cached

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

                self.cache.set(
                    file.id,
                    stats,
                )

            total_counter.update(stats)

            per_file.append(
                FileStatistics(
                    id=file.id,
                    name=file.name,
                    statistics=DigitStatistics(counts=stats),
                )
            )

        total = DigitStatistics(
            counts={
                str(i): total_counter.get(
                    str(i),
                    0,
                )
                for i in range(10)
            }
        )

        return StatisticsResponse(
            total=total,
            files=per_file,
        )
