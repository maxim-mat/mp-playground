import random
import numpy as np
import math
from shapely.geometry import Point, Polygon
from utils.Benchmarking import benchmark
from utils.Metrics import *
from utils.Distances import *


def generate_random_point_around(center, radius=1.0):
    angle = random.uniform(0, 2 * 3.14159)  # Random angle
    distance = radius * random.uniform(0.5, 1)  # Random distance within given radius
    x = center[0] + distance * math.cos(angle)
    y = center[1] + distance * math.sin(angle)
    return x, y


# Function to generate a random polygon centered around a given point
def generate_random_polygon_around(center, vertex_count, radius=1.0):
    points = [generate_random_point_around(center, radius) for _ in range(vertex_count)]
    polygon = Polygon(points)
    return polygon


def generate_polygons(n, vertex_count=10, randomize=True):
    if randomize:
        return [
            generate_random_polygon_around(
                center=(random.uniform(-1000, 1000), random.uniform(-1000, 1000)),
                vertex_count=math.ceil(random.uniform(10, 50)),
                radius=random.uniform(0, 100)
            )
            for _ in range(n)]
    else:
        return [
            generate_random_polygon_around(
                center=(random.uniform(-1000, 1000), random.uniform(-1000, 1000)),
                vertex_count=vertex_count,
                radius=random.uniform(0, 100)
            )
            for _ in range(n)]


if __name__ == '__main__':
    benchmark_functions = False
    random_polygons = generate_polygons(5)

    distances = np.zeros((len(random_polygons), len(random_polygons)))
    distances_mp = np.zeros((len(random_polygons), len(random_polygons)))
    distances_async = np.zeros((len(random_polygons), len(random_polygons)))
    update_distances_base(distances, random_polygons, euclidean)
    # update_distances_mp(distances_mp, random_polygons, euclidean)
    update_distances_threaded(distances_async, random_polygons, euclidean)
    # assert np.array_equal(distances, distances_mp)
    # assert np.array_equal(distances, distances_async)
    print(distances)
    # print(distances_mp)
    print(distances_async)

    if benchmark_functions:
        mu, sigma, (_, right) = benchmark(0.99, 100, 10, update_distances_base, distances, random_polygons, euclidean)
        print(f"function {update_distances_base.__name__} runtime: {mu}s ± {right - mu}s std div {sigma}")

        mu, sigma, (_, right) = benchmark(0.99, 100, 10, update_distances_comprehension, random_polygons, euclidean)
        print(f"function {update_distances_comprehension.__name__} runtime: {mu}s ± {right - mu}s std div {sigma}")


