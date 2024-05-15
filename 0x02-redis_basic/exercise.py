#!/usr/bin/env python3
"""Module for redis task"""
from uuid import uuid4
from typing import Union, Callable, Optional
import redis


class Cache:
    """class docstring"""
    def __init__(self) -> None:
        """ init instance of redis and flush"""
        self._redis = redis.Redis()  # Create a Redis client instance
        self._redis.flushdb()

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
