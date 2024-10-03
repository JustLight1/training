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
import aiohttp
import json


urls = [
    'https://example.com',
    'https://httpbin.org/status/404',
    'https://nonexistent.url'
]


async def fetch_urls(urls: list[str], file_path: str):
    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [load_to_json(session, url, file_path) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)


async def load_to_json(session, url: str, file_path: str):
    with open(file_path, 'a') as file:
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

        json.dump(result, file)
        file.write('\n')

if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
