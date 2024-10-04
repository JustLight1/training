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
from aiofiles import open as aio_open


urls = [
    'https://example.com',
    'https://example.com',
    'https://example.com',
    'https://httpbin.org/status/404',
    'https://httpbin.org/status/404',
    'https://httpbin.org/status/404',
    'https://nonexistent.url',
    'https://nonexistent.url',
    'https://nonexistent.url',
    'https://nonexistent.url',
]


semaphore = asyncio.Semaphore(5)


async def load_to_json(
        session: aiohttp.ClientSession,
        queue: asyncio.Queue,
        file_path: str
):
    while True:
        url = await queue.get()
        if url is None:
            queue.task_done()
            break
        async with semaphore:
            try:
                async with session.get(url, timeout=5) as response:
                    status_code = response.status
                    result = {'url': url, 'status_code': status_code}
            except aiohttp.ClientError as e:
                print(f'Error: {e}')
                result = {'url': url, 'status_code': 0}
            except asyncio.TimeoutError:
                print(f'Время ожидания истекло при запросе {url}')
                result = {'url': url, 'status_code': 408}
            except Exception as e:
                print(f'Непредвиденная ошибка при запросе {url}: {e}')
                result = {'url': url, 'status_code': -1}

            async with aio_open(file_path, 'a') as file:
                await file.write(json.dumps(result) + '\n')

        queue.task_done()


async def fetch_urls(urls: list[str], file_path: str):
    queue = asyncio.Queue(5)
    async with aiohttp.ClientSession() as session:
        workers = [asyncio.create_task(
            load_to_json(session, queue, file_path)) for _ in range(5)]
        for url in urls:
            await queue.put(url)

        await queue.join()

        for _ in workers:
            await queue.put(None)

        await asyncio.gather(*workers)


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
