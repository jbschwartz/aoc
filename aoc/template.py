import logging
from typing import TextIO, Tuple


def run(file: TextIO) -> Tuple[int, int]:
    """Run both parts for this day."""
    part_one, part_two = 0, 0

    for line in file:
        logging.debug(line.strip())

    return part_one, part_two


def one(file: TextIO) -> Tuple[int, int]:
    """Run the first part for this day."""
    result = 0

    for line in file:
        logging.debug(line.strip())

    return result


def two(file: TextIO) -> Tuple[int, int]:
    """Run the second part for this day."""
    result = 0

    for line in file:
        logging.debug(line.strip())

    return result
