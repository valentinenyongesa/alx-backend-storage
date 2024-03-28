#!/usr/bin/env python3

"""
Main file
"""

import redis
from typing import Callable

def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function.

    Args:
        method (Callable): The method for which the history of calls needs to be displayed.
    """
    redis_client = redis.Redis()
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    num_calls = min(len(inputs), len(outputs))

    print("{} was called {} times:".format(method.__qualname__, num_calls))
    for input_data, output_data in zip(inputs, outputs):
        input_args = eval(input_data.decode())
        print("{}{} -> {}".format(method.__qualname__, input_args, output_data.decode()))

class Cache:
    """
    Cache class for storing data in Redis.
    """

    def __init__(self) -> None:
        """
        Initialize Cache with a Redis client instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str) -> str:
        """
        Store the input data in Redis using a randomly generated key and return the key.

        Args:
            data (str): The data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = 'random_key'  # Placeholder for the actual key generation logic
        self._redis.set(key, data)
        return key

if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    replay(cache.store)
