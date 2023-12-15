from typing import TextIO, Tuple


def deltas(data: list[int]) -> list[int]:
    return [b - a for a, b in zip(data, data[1:])]


def get_series(file: TextIO) -> list[list[int]]:
    """Return a list of integers for every line in the file."""
    return [list(map(int, line.split())) for line in file]


def get_step(data: list[int], index: int = 0) -> list[int]:
    if all(value == 0 for value in data):
        return []

    return [data[index], *get_step(deltas(data), index)]


def subtract(data: list[int]) -> int:
    if len(data) == 1:
        return data[0]

    data[-2] = data[-2] - data[-1]
    data.pop()

    return subtract(data)


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    result = 0

    for series in get_series(file):
        # Use the end of the list to compute steps.
        result += sum(get_step(series, -1))

    return result


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    result = 0

    for series in get_series(file):
        result += subtract(get_step(series))

    return result
