from fastapi import APIRouter, Depends

from app.dependencies.statistics import get_statistics_service
from app.schemas.statistics import StatisticsRequest, StatisticsResponse
from app.services.statiscics_service import StatisticsService

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


@router.post(
    "",
    response_model=StatisticsResponse,
)
async def calculate_statistics(
    request: StatisticsRequest,
    service: StatisticsService = Depends(
        get_statistics_service,
    ),
):
    return await service.calculate(request.file_ids)
