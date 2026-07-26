import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

import httpx
from app.core.logging import get_logger
from app.integrations.external_api.exceptions import (
    ExternalApiBlockedException,
    ExternalApiRateLimitException,
)

logger = get_logger(__name__)
T = TypeVar("T")


class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 5,
        min_delay: float = 0.3,
        max_delay: float = 0.7,
    ):
        self.max_attempts = max_attempts
        self.min_delay = min_delay
        self.max_delay = max_delay

    async def execute(
        self,
        func: Callable[[], Awaitable[T]],
    ) -> T:

        attempt = 1

        while True:
            try:
                result = await func()

                # Небольшая пауза между успешными запросами,
                # чтобы не словить rate limit.
                await asyncio.sleep(
                    random.uniform(
                        self.min_delay,
                        self.max_delay,
                    )
                )

                return result

            except ExternalApiRateLimitException as exc:
                if attempt >= self.max_attempts:
                    raise

                retry_after = (
                    exc.retry_after if exc.retry_after is not None else 2**attempt
                )

                logger.warning(
                    "Rate limit exceeded. Waiting %d seconds (attempt %d/%d).",
                    retry_after,
                    attempt,
                    self.max_attempts,
                )

                await asyncio.sleep(retry_after)

            except ExternalApiBlockedException:
                raise

            except (
                httpx.RemoteProtocolError,
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.WriteTimeout,
                httpx.PoolTimeout,
            ) as exc:
                if attempt >= self.max_attempts:
                    raise

                delay = min(2**attempt, 10)

                logger.warning(
                    "Network error (%s). Retry in %d sec (%d/%d)",
                    type(exc).__name__,
                    delay,
                    attempt,
                    self.max_attempts,
                )

                await asyncio.sleep(delay)

            attempt += 1
