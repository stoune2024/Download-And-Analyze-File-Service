from fastapi import Depends

from app.dependencies.uow import get_uow
from app.factories.download_service_factory import get_storage
from app.services.statiscics_service import StatisticsService
from app.unit_of_work.uow import UnitOfWork


def get_statistics_service(
    uow: UnitOfWork = Depends(get_uow),
):

    return StatisticsService(
        storage=get_storage(),
        uow=uow,
    )
