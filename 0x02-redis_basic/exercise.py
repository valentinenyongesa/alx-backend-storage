#!/usr/bin/env python3

"""
Main file
"""

import redis
import uuid
from typing import Callable, Union

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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key and return the key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis for the given key. Optionally, apply a conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Callable, optional): A callable function to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data from Redis.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from Redis for the given key and convert it to a UTF-8 encoded string.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Union[str, None]: The retrieved data as a UTF-8 encoded string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from Redis for the given key and convert it to an integer.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Union[int, None]: The retrieved data as an integer.
        """
        return self.get(key, fn=int)

if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
