
import httpx

from app.integrations.external_api.exceptions import (
    ExternalApiBlockedException,
    ExternalApiRateLimitException,
)
from app.integrations.external_api.retry import (
    RetryPolicy,
)
from app.integrations.external_api.schemas import (
    DownloadedResponse,
    DownloadRequest,
    FileNamesResponse,
)


class ExternalApiClient:
    def __init__(
        self,
        base_url: str,
        candidate_id: str | None,
        timeout: int,
        retry_policy: RetryPolicy,
    ):

        self.base_url = base_url.rstrip("/")

        self.retry_policy = retry_policy

        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers={"X-Candidate-Id": candidate_id} if candidate_id else {},
        )

    async def get_names(self) -> list[str]:

        async def request():

            response = await self.client.get(f"{self.base_url}/api/files/names")

            await self._handle_errors(response)

            data = FileNamesResponse.model_validate(response.json())

            return data.file_names

        return await self.retry_policy.execute(request)

    async def download(
        self,
        file_names: list[str],
    ) -> bytes:

        async def request():

            payload = DownloadRequest(file_names=file_names)

            response = await self.client.post(
                f"{self.base_url}/api/files/download",
                json=payload.model_dump(),
            )

            await self._handle_errors(response)

            return response.content

        return await self.retry_policy.execute(request)

    async def mark_downloaded(
        self,
        file_names: list[str],
    ) -> DownloadedResponse:

        async def request():

            response = await self.client.post(
                f"{self.base_url}/api/files/downloaded",
                json={"file_names": file_names},
            )

            await self._handle_errors(response)

            return DownloadedResponse.model_validate(response.json())

        return await self.retry_policy.execute(request)

    async def _handle_errors(
        self,
        response: httpx.Response,
    ):

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))

            raise ExternalApiRateLimitException(retry_after)

        if response.status_code == 403:
            retry_after = response.headers.get("Retry-After")

            raise ExternalApiBlockedException(int(retry_after) if retry_after else None)

        response.raise_for_status()
