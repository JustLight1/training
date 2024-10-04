"""
Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и
возвращает словарь, где ключами являются URL, а значениями — статус-коды
ответов. Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:

Ограничьте количество одновременных запросов до 5.
Обработайте возможные исключения (например, таймауты, недоступные ресурсы) и
присвойте соответствующие статус-коды (например, 0 для ошибок соединения).
Сохраните все результаты в файл
"""


import asyncio
import json

import aiohttp
import aiofiles


urls = [
    'https://example.com',
    'https://httpbin.org/status/404',
    'https://nonexistent.url',
]


async def worker(q_in: asyncio.Queue, q_out: asyncio.Queue):
    while True:
        url = await q_in.get()
        q_in.task_done()

        if url is None:
            break

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    status_code = response.status
        except aiohttp.ClientError as e:
            print(f'Error: {e}')
            status_code = 0
        except asyncio.TimeoutError:
            print(f'Время ожидания истекло при запросе {url}')
            status_code = 408
        except Exception as e:
            print(f'Непредвиденная ошибка при запросе {url}: {e}')
            status_code = 0
        result = {'url': url, 'status_code': status_code}

        await q_out.put(result)


async def consumer(q: asyncio.Queue):
    while True:
        result = await q.get()
        q.task_done()

        if result is None:
            break

        async with aiofiles.open('./results.jsonl', 'a') as file:
            await file.write(json.dumps(result) + '\n')


async def main():
    queue_in = asyncio.Queue(maxsize=5)
    queue_out = asyncio.Queue(maxsize=5)

    workers = [asyncio.create_task(
        worker(queue_in, queue_out)) for _ in range(5)]

    asyncio.create_task(consumer(queue_out))

    for url in urls:
        await queue_in.put(url)
    await queue_in.join()

    for _ in workers:
        await queue_in.put(None)

    await queue_in.join()

    await queue_out.put(None)

    await queue_out.join()


if __name__ == '__main__':
    asyncio.run(main())
