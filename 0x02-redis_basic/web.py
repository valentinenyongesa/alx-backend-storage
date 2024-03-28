#!/usr/bin/env python3

"""
web.py
"""

import requests
import redis
import functools
import time

def track_access(func):
    """
    Decorator to track the number of times a URL was accessed.
    """
    @functools.wraps(func)
    def wrapper_track_access(url):
        # Initialize Redis client
        redis_client = redis.Redis()

        # Track the number of times the URL was accessed
        redis_key = f"count:{url}"
        redis_client.incr(redis_key)

        return func(url)
    
    return wrapper_track_access

def cache_content(func):
    """
    Decorator to cache the content of a URL with an expiration time of 10 seconds.
    """
    @functools.wraps(func)
    def wrapper_cache_content(url):
        # Initialize Redis client
        redis_client = redis.Redis()

        # Check if the page content is cached
        cached_content = redis_client.get(url)
        if cached_content:
            return cached_content.decode()

        # Fetch the page content
        content = func(url)

        # Cache the page content with an expiration time of 10 seconds
        redis_client.setex(url, 10, content)

        return content
    
    return wrapper_cache_content

@track_access
@cache_content
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and returns it.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com"
    start_time = time.time()
    content = get_page(url)
    end_time = time.time()
    print(f"Time taken to fetch content: {end_time - start_time} seconds")
    print(content)
