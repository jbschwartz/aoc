import logging
from functools import reduce
from typing import TextIO, Tuple

MAXIMUMS = {"red": 12, "green": 13, "blue": 14}


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    # for id, line in enumerate(file, 1):

    #     valid = True
    #     draws = line.strip().split(":")[1].split(";")
    #     for draw in draws:
    #         for pair in draw.split(","):
    #             num, color = pair.strip().split(" ")
    #             if int(num) > MAXIMUMS[color]:
    #                 valid = False

    #     if valid:
    #         part_one += id

    for line in file:
        minimums = {"red": 0, "green": 0, "blue": 0}
        draws = line.strip().split(":")[1].split(";")
        for draw in draws:
            for pair in draw.split(","):
                num, color = pair.strip().split(" ")
                if int(num) > minimums[color]:
                    minimums[color] = int(num)

        part_two += reduce(lambda x, y: x * y, minimums.values(), 1)

    return part_one, part_two
