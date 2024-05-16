#!/usr/bin/env python3
"""Module for redis task"""
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """count the number of time a class Cache methode is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """some documentation"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """count the number of time a class Cache methode is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """some documentation"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store inputs as a string
        self._redis.rpush(input_key, str(args))

        # Execute the method and store the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache:
    """class docstring"""
    def __init__(self) -> None:
        """ init instance of redis and flush"""
        self._redis = redis.Redis()  # Create a Redis client instance
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        """method that takes a data argument and returns a string"""
        random_key = str(uuid4())
        # Store data in Redis with the generated key
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get data with key """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """
        Retrieves data from Redis, converts it to an integer, and returns it.
        """
        data = self._redis.get(key).decode("utf-8")
        return data

    def get_int(self, key: str) -> int:
        """
        Retrieves data from Redis, converts it to an integer, and returns it.
        """
        data = int(self._redis.get(key).decode("utf-8"))
        return data
