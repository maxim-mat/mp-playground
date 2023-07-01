import numpy as np
import multiprocessing as mp
import asyncio


N_CPU = mp.cpu_count()


def update_distances_base(distances, objects, metric, indexes=None):
    if indexes is None:
        indexes = range(len(objects))
    for i, x in enumerate(objects):
        for j, y in enumerate(objects):
            if i < j and j in indexes:
                distances[i, j] = distances[j, i] = metric(x, y)


def update_distances_comprehension(objects, metric):
    return [[metric(x, y) for y in objects] for x in objects]


def update_distances_mp(distances, objects, metric, workers=N_CPU):
    def update_distances_inner(indexes):
        return update_distances_base(distances, objects, metric, indexes)

    with mp.Pool(workers) as pool:
        return pool.map(update_distances_inner, np.array_split(range(len(objects)), workers))


async def update_distances_threaded(distances, objects, metric, workers=N_CPU):
    async def update_distance_inner(indexes):
        return update_distances_base(distances, objects, metric, indexes)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [loop.create_task(update_distance_inner(chunk)) for chunk in np.array_split(range(len(objects)), workers)]
    await asyncio.gather(*tasks)
