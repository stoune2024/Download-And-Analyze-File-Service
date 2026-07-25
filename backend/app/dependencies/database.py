from functools import lru_cache

from app.core.config import settings
from app.core.database import Database


@lru_cache
def get_database() -> Database:
    return Database(settings)