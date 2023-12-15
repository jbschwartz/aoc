import enum
from functools import reduce
from typing import TextIO, Tuple


class Colors(enum.Enum):
    RED = 12
    GREEN = 13
    BLUE = 14


def parse(line: str) -> list[tuple[int, str]]:
    """Return a list of draws for the given game"""
    game = line.strip().split(":")[1].split(";")

    draws = []
    for draw in game:
        for pair in draw.split(","):
            number, color = pair.strip().split(" ")
            draws.append((int(number), Colors[color.upper()]))

    return draws


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    result = 0

    for id, line in enumerate(file, 1):
        if all(number <= color.value for number, color in parse(line)):
            result += id

    return result


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    result = 0

    for line in file:
        minimums = {Colors.RED: 0, Colors.GREEN: 0, Colors.BLUE: 0}

        for number, color in parse(line):
            if number > minimums[color]:
                minimums[color] = number

        # Get the product of all three values.
        result += reduce(lambda x, y: x * y, minimums.values(), 1)

    return result
