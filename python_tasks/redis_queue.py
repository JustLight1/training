"""
Реализуйте класс очереди который использует редис под капотом
"""
import json

import redis


class RedisQueue:
    def __init__(
            self, queue_name='redis_queue', host='localhost', port='6379'
    ):
        self.redis_client = redis.Redis(host=host, port=port)
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
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
