import math
import multiprocessing as mp
import scipy.stats as st
import time
import numpy as np
import asyncio

SAMPLE_SIZE = 100
SAMPLES = 10


def timeit(func):

    def timed_func(*args, **kwargs):
        ts = time.time()
        res = func(*args, **kwargs)
        te = time.time()
        return (te - ts), res, func.__name__

    return timed_func


def benchmark(func, sample_size=100, samples=10, *args, **kwargs):
    times = []

    @timeit
    def timed_func():
        return func(*args, **kwargs)

    for i in range(samples):
        accumulator = 0
        for j in range(sample_size):
            ts = time.time()
            func(*args, **kwargs)
            te = time.time()
            accumulator += te - ts
        times.append(accumulator / sample_size)

    return np.average(times), st.sem(times), len(times) - 1


def f(arr):
    return [math.sin(x**2 + 5) for x in arr]


async def f2(arr):
    return f(arr)

def f_mp(arr):
    n_workers = 4
    with mp.Pool(n_workers) as pool:
        return pool.map(f, np.array_split(arr, n_workers))

async def f_threaded(arr, loop):
    n_workers = 4
    # chunk_size = len(arr) // n_workers
    # chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]
    chunks = np.array_split(arr, n_workers)

    # loop = asyncio.get_event_loop()
    tasks = [loop.create_task(f2(chunk)) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    return np.concatenate(results)

def main():
    arr = list(range(10000000))

    ts = time.time()
    f(arr)
    print('Single process single thread (sync): ', time.time() - ts)
    ts = time.time()
    f_mp(arr)
    print('Multi process single thread: ', time.time() - ts)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ts = time.time()
    loop.run_until_complete(f2(arr))
    print('Single process single thread (async): ', time.time() - ts)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ts = time.time()
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(f_threaded(arr, loop))
    print('Single process multi thread: ', time.time() - ts)

if __name__ == "__main__":
    main()
