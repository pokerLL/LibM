import functools
import json

import redis
from django.http import HttpResponse, JsonResponse


# django_version 3.1.2
# redis_version 3.2.1
# redis_pack_version 2.10.6

class RedisLRUCacheDict:

    def __init__(self):
        # 初始化一个连接池
        self.conn_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=20, decode_responses=True)
        redis.Redis(connection_pool=self.conn_pool).flushdb()

    def push(self, key, value, expiration=60, redis_conn=None):
        # print("pushing ->", key, value)
        if redis_conn is None:
            redis_conn = redis.Redis(connection_pool=self.conn_pool, decode_responses=True)
        self.delete(key, redis_conn=redis_conn)
        redis_conn.set(key, value, ex=expiration)

    def getitem(self, key, redis_conn=None):
        if redis_conn is None:
            redis_conn = redis.Redis(connection_pool=self.conn_pool, decode_responses=True)
        # print(redis_conn.get(key))
        return redis_conn.get(key)

    def __contains__(self, key):
        return key in redis.Redis(connection_pool=self.conn_pool, decode_responses=True).keys()

    def delete(self, key, redis_conn=None):
        # print("deleteing ->", key)
        if redis_conn is None:
            redis_conn = redis.Redis(connection_pool=self.conn_pool, decode_responses=True)
        if key in redis_conn.keys():
            redis_conn.delete(key)


CACHE = RedisLRUCacheDict()


def cache_it_httpresponse(expiration=600, prefix=""):
    def wrapper(func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            keyp = prefix
            try:
                keyp = keyp + func.__name__ + str(args) + str(kwargs)
            except:
                keyp = keyp + func.__name__
            if request.method == "POST":
                keyp = keyp + str(request.POST.dict())
            result = CACHE.getitem(keyp)
            if result is None:
                print("load ", keyp)
                result = func(request, *args, **kwargs).content.decode('utf-8')
                CACHE.push(keyp, result, expiration)
                # print(type(result))
            else:
                print("hit ", keyp)
            return HttpResponse(result)

        return inner

    return wrapper


def cache_it_json(expiration=600, prefix=""):
    def wrapper(func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            keyp = prefix
            try:
                keyp = keyp + func.__name__ + str(args) + str(kwargs)
            except:
                keyp = keyp + func.__name__
            if request.method == "POST":
                keyp = keyp + str(request.POST.dict())
            result = CACHE.getitem(keyp)
            if result is None:
                print("load ", keyp)
                result = func(request, *args, **kwargs).content.decode('utf-8')
                CACHE.push(keyp, result, expiration)
                # print(result)
            else:
                print("hit ", keyp)
            return JsonResponse(json.loads(result), safe=False)

        return inner

    return wrapper


def cache_it_func(expiration=60, prefix=""):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            keyp = prefix
            try:
                keyp = keyp + func.__name__ + str(args) + str(kwargs)
            except:
                keyp = keyp + func.__name__
            result = CACHE.getitem(keyp)
            if result is None:
                print("load ", keyp)
                result = func(*args, **kwargs)
                CACHE.push(keyp, result, expiration)
            else:
                print("hit ", keyp)
            return result

        return inner

    return wrapper
