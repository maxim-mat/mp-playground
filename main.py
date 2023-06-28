import multiprocessing as mp
import scipy.stats as st
import time
import numpy as np

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
    return [x**2 for x in arr]


def f_mp(arr):
    n_workers = 4
    with mp.Pool(n_workers) as pool:
        return pool.map(f, np.array_split(arr, n_workers))


def main():
    ts = time.time()
    f(list(range(100000)))
    print(time.time() - ts)
    ts = time.time()
    f_mp(list(range(100000)))
    print(time.time() - ts)


if __name__ == "__main__":
    main()
