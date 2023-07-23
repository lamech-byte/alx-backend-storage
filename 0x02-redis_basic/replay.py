#!/usr/bin/env python3

from exercise import Cache, replay

if __name__ == "__main__":
    cache = Cache()
    key1 = cache.store("foo")
    key2 = cache.store("bar")
    key3 = cache.store(42)

    # Call the replay function for the cache.store method
    replay(cache, cache.store)
