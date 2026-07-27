from fastapi import Depends

from app.dependencies.uow import get_uow
from app.services.file_service import (
    FileService,
)
from app.unit_of_work.uow import UnitOfWork


def get_file_service(
    uow: UnitOfWork = Depends(get_uow),
):

    return FileService(uow)
