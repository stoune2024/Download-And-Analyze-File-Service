class ExternalApiException(Exception):
    pass


class ExternalApiBlockedException(ExternalApiException):
    """
    403 - клиент заблокирован.
    """

    def __init__(
        self,
        retry_after: int | None = None,
    ):
        self.retry_after = retry_after

        super().__init__(f"External API blocked. Retry after {retry_after}s")


class ExternalApiRateLimitException(ExternalApiException):
    """
    429 - превышен лимит запросов.
    """

    def __init__(
        self,
        retry_after: int,
    ):
        self.retry_after = retry_after

        super().__init__("External API rate limit exceeded")
