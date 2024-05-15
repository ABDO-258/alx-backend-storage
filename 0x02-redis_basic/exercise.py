#!/usr/bin/env python3
"""Module for redis task"""
from uuid import uuid4
from typing import Union
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
