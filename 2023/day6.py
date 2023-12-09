import logging
import math
from typing import TextIO, Tuple


def quadratic(a, b, c):
    root = math.sqrt(b**2 - (4 * a * c))
    return (-b + root) / (2 * a), (-b - root) / (2 * a)


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 1, 0

    times = file.readline().strip().split()[1:]
    distances = file.readline().strip().split()[1:]

    for time, distance in zip(times, distances):
        low, high = quadratic(-1, int(time), -int(distance))

        delta = math.floor(high) - math.ceil(low) + 1

        if math.floor(high) == high:
            delta -= 1

        if math.ceil(low) == low:
            delta -= 1

        part_one *= delta

    time = "".join(times)
    distance = "".join(distances)

    low, high = quadratic(-1, int(time), -int(distance))

    delta = math.floor(high) - math.ceil(low) + 1

    if math.floor(high) == high:
        delta -= 1

    if math.ceil(low) == low:
        delta -= 1

    part_two = delta

    return part_one, part_two
