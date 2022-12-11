import logging
from typing import TextIO, Tuple


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    for line in file:
        logging.debug(line.strip())

    return part_one, part_two
