

import math


def DistanceMetric(first, second) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(first, second)))


