import time
import numpy as np
from scipy import stats
from tqdm import tqdm


def timeit(func, *args, **kwargs):
    ts = time.time()
    res = func(*args, **kwargs)
    return time.time() - ts, res


def benchmark(confidence, samples, sample_size, func, *args, **kwargs):
    runtimes = []
    for _ in tqdm(range(samples)):
        sample_avg = 0
        for j in range(sample_size):
            runtime, _ = timeit(func, *args, **kwargs)
            sample_avg += (runtime - sample_avg) / (j + 1)
        runtimes.append(sample_avg)

    mean = np.mean(runtimes)
    std = stats.sem(runtimes)

    return mean, std, stats.t.interval(confidence, samples - 1, loc=mean, scale=std)
