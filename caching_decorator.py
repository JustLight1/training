"""
Этот декоратор должен кешировать результаты вызовов функции на основе её
аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте
результат из кеша вместо повторного выполнения функции.
Реализуйте кеширование с использованием словаря, где ключами будут аргументы
функции, а значениями — результаты её выполнения.
Ограничьте размер кеша до 100 записей. При превышении этого лимита удаляйте
наиболее старые записи (используйте подход FIFO).
"""


def cache_decorator(max_size=100):
    def decorator(func):
        cache = {}

        def wrapper(*args, **kwargs):
            key = args

            if key in cache:
                return cache[key]
            else:
                result = func(*args, **kwargs)
                cache[key] = result

                if len(cache) > max_size:
                    first_key = next(iter(cache))
                    del cache[first_key]

                return result

        return wrapper

    return decorator


@cache_decorator(max_size=100)
def sum_func(a, b):
    return a + b
