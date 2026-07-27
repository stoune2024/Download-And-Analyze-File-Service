from functools import lru_cache


class StatisticsCache:
    def __init__(self):
        self._cache: dict[int, dict[str, int]] = {}

    def get(self, key: int):
        return self._cache.get(key)

    def set(
        self,
        key: int,
        value: dict[str, int],
    ):
        self._cache[key] = value


@lru_cache
def get_statistics_cache() -> StatisticsCache:
    return StatisticsCache()
