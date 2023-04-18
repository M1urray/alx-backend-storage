#!/usr/bin/env python3
''' Redis Module '''
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    ''' Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Invokes the given method after incrementing its call counter 
        '''
        
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' def call history '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' def wrapper'''
        key_m = method.__qualname__
        inp_m = key_m + ':inputs'
        outp_m = key_m + ":outputs"
        data = str(args)
        self._redis.rpush(inp_m, data)
        fin = method(self, *args, **kwargs)
        self._redis.rpush(outp_m, str(fin))
        return fin
    return wrapper


def replay(func: Callable):
    '''def replay'''
    r = redis.Redis()
    key_m = func.__qualname__
    inp_m = r.lrange("{}:inputs".format(key_m), 0, -1)
    outp_m = r.lrange("{}:outputs".format(key_m), 0, -1)
    calls_number = len(inp_m)
    times_str = 'times'
    if calls_number == 1:
        times_str = 'time'
    fin = '{} was called {} {}:'.format(key_m, calls_number, times_str)
    print(fin)
    for k, v in zip(inp_m, outp_m):
        fin = '{}(*{}) -> {}'.format(
            key_m,
            k.decode('utf-8'),
            v.decode('utf-8')
        )
        print(fin)


class Cache():
    ''' class cache '''
    def __init__(self):
        ''' def init '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' def store '''
        gen = str(uuid.uuid4())
        self._redis.set(gen, data)
        return gen

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        ''' def get '''
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key):
        '''define the get int function
        '''
        return self.get(key, int)

    def get_str(self, key):
        '''define the get str function
        '''
        value = self._redis.get(key)
        return value.decode("utf-8")
