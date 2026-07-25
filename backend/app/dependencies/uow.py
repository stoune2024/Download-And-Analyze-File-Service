from fastapi import Depends

from app.core.database import Database
from app.dependencies.database import get_database
from app.unit_of_work.uow import UnitOfWork


def get_uow(
    database: Database = Depends(get_database),
) -> UnitOfWork:
    return UnitOfWork(database)