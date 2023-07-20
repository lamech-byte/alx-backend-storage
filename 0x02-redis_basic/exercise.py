#!/usr/bin/env python3

import redis
import uuid


class Cache:
    def __init__(self):
        self._redis = redis.Redis()

    def store(self, data):
        # Generate a random key
        key = str(uuid.uuid4())
        # Store the data as a byte string
        self._redis.set(key, data)
        # Return the key
        return key

    def get(self, key, fn=None):
        # Get the data from the key
        data = self._redis.get(key)
        # If key does not exist, return None
        if data is None:
            return None
        # If fn is provided, apply it to the data
        if fn:
            data = fn(data)
        # Return the data
        return data

    def get_str(self, key):
        # Get the data as a UTF-8 string
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key):
        # Get the data as an integer
        return self.get(key, fn=int)
