from functools import lru_cache

from app.core.config import settings
from app.integrations.external_api.client import (
    ExternalApiClient,
)
from app.integrations.external_api.retry import (
    RetryPolicy,
)


@lru_cache
def get_external_api_client():

    return ExternalApiClient(
        base_url=settings.external_api_url,
        candidate_id=settings.candidate_id,
        timeout=settings.request_timeout,
        retry_policy=RetryPolicy(settings.max_retries),
    )
