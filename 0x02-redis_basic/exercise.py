#!/usr/bin/env python3

"""
Main file
"""

import redis
import uuid
from functools import wraps
from typing import Callable, Union

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method of the Cache class is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls and call the original method.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            The result of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

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

    @count_calls
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

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))
