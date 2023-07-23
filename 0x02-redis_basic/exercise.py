#!/usr/bin/env python3

import redis
import uuid
from typing import Callable, Union
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method that counts the number of calls.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that records the inputs and outputs of a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method that records the inputs and outputs.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_list_key = "{}:inputs".format(method.__qualname__)
        output_list_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(input_list_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_list_key, result)

        return result

    return wrapper


class Cache:
    """
    A class that provides caching functionality using Redis.

    Attributes:
        _redis (redis.Redis): The Redis client instance.
    """
    def __init__(self):
        """Initialize the Redis cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache and return the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in the cache.

        Returns:
            str: The key associated with the stored data.
        """
        # Generate a random key
        key = str(uuid.uuid4())
        # Store the data as a byte string
        self._redis.set(key, data)
        # Return the key
        return key

    def get(self, key, fn=None) -> Union[str, bytes, int, float, None]:
        """
        Get the data from the cache using the given key.

        Args:
            key: The key used to retrieve the data from the cache.
            fn (Callable, optional): A function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data from the cache.
        """
        # Get the data from the key
        data = self._redis.get(key)
        # If key does not exist, return None
        if data is None:
            return None
        # If fn is provided apply it to the data
        if fn:
            data = fn(data)
        # Return the data
        return data

    def get_str(self, key) -> str:
        """
        Get the data from the cache as a UTF-8 string.

        Args:
            key: The key used to retrieve the data from the cache.

        Returns:
            str: The retrieved data as a UTF-8 string.
        """
        # Get the data as a UTF-8 string
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key) -> int:
        """
        Get the data from the cache as an integer.

        Args:
            key: The key used to retrieve the data from the cache.

        Returns:
            int: The retrieved data as an integer.
        """
        # Get the data as an integer
        return self.get(key, fn=int)


def replay(cache: Cache, method: Callable) -> None:
    """Replay the calls to a method from the cache."""
    input_list_key = "{}:inputs".format(method.__qualname__)
    output_list_key = "{}:outputs".format(method.__qualname__)

    inputs = [eval(args_str.decode("utf-8"))
              for args_str in cache._redis.lrange(input_list_key, 0, -1)]
    outputs = cache._redis.lrange(output_list_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}{args} -> {output.decode()}")
