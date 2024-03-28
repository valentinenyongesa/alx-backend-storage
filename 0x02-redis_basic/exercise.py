#!/usr/bin/env python3

"""
Main file
"""

import redis
import uuid
from typing import Callable

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history in Redis.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments passed to the method.

        Returns:
            The result of the original method.
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        input_data = str(args)
        
        self._redis.rpush(input_key, input_data)
        
        output_data = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output_data)
        
        return output_data
    
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

    @call_history
    def store(self, data: str) -> str:
        """
        Store the input data in Redis using a randomly generated key and return the key.

        Args:
            data (str): The data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
