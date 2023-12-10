import math
from typing import TextIO, Tuple


def compute_number_of_winners(time, distance) -> int:
    """Compute the number of winning strategies for the given time and distance."""
    low, high = quadratic(-1, int(time), -int(distance))

    delta = math.floor(high) - math.ceil(low) + 1

    # Do not count the roots of the equation if they are integers since those would represent ties.
    if math.floor(high) == high:
        delta -= 1

    if math.ceil(low) == low:
        delta -= 1

    return delta


def quadratic(a, b, c):
    root = math.sqrt(b**2 - (4 * a * c))
    return (-b + root) / (2 * a), (-b - root) / (2 * a)


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 1, 0

    times = file.readline().strip().split()[1:]
    distances = file.readline().strip().split()[1:]

    for time, distance in zip(times, distances):
        part_one *= compute_number_of_winners(time, distance)

    time = "".join(times)
    distance = "".join(distances)

    part_two = compute_number_of_winners(time, distance)

    return part_one, part_two
