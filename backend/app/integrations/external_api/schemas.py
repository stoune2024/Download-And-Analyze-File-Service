from pydantic import BaseModel


class FileNamesResponse(BaseModel):
    file_names: list[str]


class DownloadRequest(BaseModel):
    file_names: list[str]


class DownloadedResponse(BaseModel):
    marked_now: int
    already_marked: int
