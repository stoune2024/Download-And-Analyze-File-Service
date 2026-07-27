from pydantic import BaseModel


class StatisticsRequest(BaseModel):
    file_ids: list[int]


class DigitStatistics(BaseModel):
    counts: dict[str, int]


class FileStatistics(BaseModel):
    id: int

    name: str

    statistics: DigitStatistics


class StatisticsResponse(BaseModel):
    total: DigitStatistics

    files: list[FileStatistics]
