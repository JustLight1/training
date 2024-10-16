"""
У вас есть распределенное приложение работающее на десятках серверах. Вам
необходимо написать декоратор single который гарантирует, что декорируемая
функция не исполняется параллельно.

Пример использования:

Параметр max_processing_time указывает на максимально допустимое время работы
декорируемой функции.
"""
import datetime
import time
from functools import wraps

import redis


redis_client = redis.StrictRedis(host='localhost', port=6379)


def single(max_processing_time: datetime.timedelta):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            lock_key = f'lock:{func.__name__}'
            with redis_client.lock(
                lock_key, timeout=max_processing_time.total_seconds(),
                blocking=False
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(minutes=1))
def process_transaction():
    time.sleep(2)
