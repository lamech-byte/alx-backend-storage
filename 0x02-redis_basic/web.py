#!/usr/bin/env python3

import requests
import redis
import time


def get_page(url: str) -> str:
    # Connect to Redis
    r = redis.Redis()

    # Check if the URL count exists in Redis
    count_key = f"count:{url}"
    url_count = r.get(count_key)

    # If the URL has not been accessed before,
    # set the count to 1 with an expiration time of 10 seconds
    if url_count is None:
        r.setex(count_key, 10, 1)
    else:
        # If the URL has been accessed before,
        # increment the count and update the expiration time
        r.incr(count_key)
        r.expire(count_key, 10)

    # Fetch the page content using requests
    response = requests.get(url)
    page_content = response.text  # Extract only the page content

    return page_content

if __name__ == "__main__":
    url = "http://google.com"
    page_content = get_page(url)
    print(f"{url} is cached for 10 seconds and removed
    from the redis cache after 10 sec")
    print(f"Page Content: {page_content}")
