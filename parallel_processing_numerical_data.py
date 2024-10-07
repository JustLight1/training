"""
Разработайте программу, которая выполняет следующие шаги:

Сбор данных:

Создайте функцию generate_data(n), которая генерирует список из n случайных
целых чисел в диапазоне от 1 до 1000. Например, generate_data(1000000) должна
вернуть список из 1 миллиона случайных чисел.

Обработка данных:

Напишите функцию process_number(number), которая выполняет вычисления над
числом. Например, вычисляет факториал числа или проверяет, является ли число
простым. Обратите внимание, что обработка должна быть ресурсоёмкой, чтобы
продемонстрировать преимущества мультипроцессинга.

Параллельная обработка:

Используйте модули multiprocessing и concurrent.futures для параллельной
обработки списка чисел.

Реализуйте три варианта:

Вариант А: Ипользование пула потоков с concurrent.futures.

Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным
количеству CPU.

Вариант В: Создание отдельных процессов с использованием
multiprocessing.Process и очередей (multiprocessing.Queue) для передачи данных.

Сравнение производительности:

Измерьте время выполнения для всех вариантов и сравните их с однопоточным
(однопроцессным) вариантом. Представьте результаты в виде таблицы или графика.

Сохранение результатов:

Сохраните обработанные данные в файл (например, в формате JSON или CSV).
"""
import csv
import multiprocessing
import os
import random
from concurrent.futures import ThreadPoolExecutor
from time import time


def decorator(func):
    """
    Декоратор для измерения времени выполнения.
    """
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        time_taken = f'{(end-start):.4f}'
        print(f'Функция {func.__name__} отработала за {time_taken} секунд!')
        return result, func.__name__, time_taken
    return wrapper


def generate_data(n):
    """
    Генерация списка рандомных данных состоящих из чисел от 1 до 1000.
    """
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number):
    """
    Функция для вычисления факториала числа.
    """
    factorial = 1
    for num in range(2, number + 1):
        factorial *= num
    return factorial


@decorator
def process_data_single_thread(data):
    results = [process_number(number) for number in data]
    return results


@decorator
def process_data_parallel(data):
    """
    Использование пула потоков с concurrent.futures.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, data))
    return results


@decorator
def process_data_multiprocessing(data):
    """
    Использование multiprocessing.Pool с пулом процессов, равным кол-ву CPU.
    """
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_number, data)
    return results


def process_chunk(chunk, queue: multiprocessing.Queue):
    """
    Функция для обработки части данных в отдельном процессе и добавления данных
    в очередь.
    """
    results = [process_number(number) for number in chunk]
    queue.put(results)


@decorator
def process_data_separate_processes(data):
    """
    Создание отдельных процессов с использованием multiprocessing.Process и
    очередей (multiprocessing.Queue) для передачи данных.
    """
    num_processes = os.cpu_count()
    chunk_size = len(data) // num_processes
    queue = multiprocessing.Queue()
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(data)
        chunk = data[start:end]
        process = multiprocessing.Process(
            target=process_chunk, args=(chunk, queue))
        processes.append(process)
        process.start()

    results = []
    for _ in range(num_processes):
        results.extend(queue.get())

    for process in processes:
        process.join()

    return results


def save_results_to_csv(results, filename='./results.csv'):
    """
    Сохраняет данные в csv файл в формате: Название функции, Время исполнения.
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Function', 'Time (seconds)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for func_name, time_taken in results:
            writer.writerow(
                {'Function': func_name, 'Time (seconds)': time_taken})


if __name__ == '__main__':
    data = generate_data(500)
    results = []

    result, func_name, time_taken = process_data_single_thread(data)
    results.append((func_name, time_taken))

    result, func_name, time_taken = process_data_parallel(data)
    results.append((func_name, time_taken))

    result, func_name, time_taken = process_data_multiprocessing(data)
    results.append((func_name, time_taken))

    result, func_name, time_taken = process_data_separate_processes(data)
    results.append((func_name, time_taken))

    save_results_to_csv(results)
