import asyncio

from app.integrations.external_api.exceptions import (
    ExternalApiBlockedException,
    ExternalApiRateLimitException,
)


class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 5,
    ):
        self.max_attempts = max_attempts

    async def execute(self, func):

        attempt = 1

        while True:
            try:
                return await func()

            except ExternalApiRateLimitException as exc:
                if attempt >= self.max_attempts:
                    raise

                await asyncio.sleep(exc.retry_after)

            except ExternalApiBlockedException:
                raise

            attempt += 1
