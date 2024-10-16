"""
Ваше приложение делает HTTP запросы в сторонний сервис
(функция make_api_request), при этом сторонний сервис имеет проблемы с
производительностью и ваша задача ограничить количество запросов к этому
сервису - не больше пяти запросов за последние три секунды. Ваша задача
реализовать RateLimiter.test метод который:

возвращает True в случае если лимит на кол-во запросов не достигнут
возвращает False если за последние 3 секунды уже сделано 5 запросов.

Ваша реализация должна использовать Redis, т.к. предполагается что приложение
работает на нескольких серверах.
"""
import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(
            self, redis_client: redis.Redis
    ):
        self.redis_client = redis_client
        self.key = 'rate_limiter'
        self.max_request = 5
        self.period = 3
        self.redis_client.delete(self.key)

    def test(self) -> bool:
        current_time = time.time()

        # Удаляем старые записи (старше временного окна)
        self.redis_client.zremrangebyscore(self.key, 0,
                                           current_time - self.period)

        # Проверяем текущее количество запросов
        current_count = self.redis_client.zcard(self.key)

        if current_count >= self.max_request:
            return False

        # Добавляем текущий запрос с временной меткой
        self.redis_client.zadd(self.key, {current_time: current_time})
        return True


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == '__main__':
    redis_client = redis.Redis(host='localhost', port=6379)
    rate_limiter = RateLimiter(redis_client)

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
