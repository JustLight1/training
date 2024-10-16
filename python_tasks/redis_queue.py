"""
Реализуйте класс очереди который использует редис под капотом
"""
import json

import redis


class RedisQueue:
    def __init__(
            self, redis_client: redis.Redis, queue_name='redis_queue'
    ):
        self.redis_client = redis_client
        self.queue_name = queue_name

    def publish(self, msg: dict):
        self.redis_client.rpush(self.queue_name, json.dumps(msg))

    def consume(self) -> dict:
        mgs = self.redis_client.lpop(self.queue_name)
        if mgs:
            try:
                return json.loads(mgs)
            except json.JSONDecodeError:
                return None
        return None


if __name__ == '__main__':
    redis_client = redis.Redis(host='localhost', port=6379)
    q = RedisQueue(redis_client)
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
