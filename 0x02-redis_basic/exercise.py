import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        if isinstance(data, (str, bytes)):
            self._redis.set(key, data)
        elif isinstance(data, (int, float)):
            self._redis.set(key, str(data))
        return key
