import logging
from typing import TextIO


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    result = 0

    for line in file:
        logging.debug(line.strip())

    return result


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    result = 0

    for line in file:
        logging.debug(line.strip())

    return result
