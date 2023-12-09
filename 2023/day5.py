import dataclasses
import functools
import logging
import math
from typing import TextIO, Tuple


@dataclasses.dataclass
class Range:
    destination_start: int
    source_start: int
    length: int

    @property
    def destination_end(self) -> int:
        return self.destination_start + self.length - 1

    @property
    def source_end(self) -> int:
        return self.source_start + self.length - 1

    def evaluate(self, source: int) -> int | None:
        if self.source_start <= source <= self.source_end:
            return self.destination_start + (source - self.source_start)

        return None


class Ranges:
    def __init__(self) -> None:
        self.ranges = []

    def add_range(self, range: Range) -> None:
        self.ranges.append(range)

    def evaluate(self, source: int) -> int:
        for range in self.ranges:
            if value := range.evaluate(source):
                return value

        return source


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    # seeds = list(map(int, file.readline().strip().split()[1:]))

    # this_ranges = None
    # maps = []

    # for line in file:
    #     line = line.strip()

    #     if not line:
    #         continue

    #     if line.endswith("map:"):
    #         if this_ranges is not None:
    #             maps.append(this_ranges)

    #         this_ranges = Ranges()

    #         continue

    #     # logging.info(line)

    #     if line[0].isdigit():
    #         params = map(int, line.split())
    #         this_ranges.add_range(Range(*params))

    # maps.append(this_ranges)

    # part_one = min(
    #     functools.reduce(lambda seed, ranges: ranges.evaluate(seed), maps, seed) for seed in seeds
    # )

    seeds = list(map(int, file.readline().strip().split()[1:]))

    this_ranges = None
    maps = []

    for line in file:
        line = line.strip()

        if not line:
            continue

        if line.endswith("map:"):
            if this_ranges is not None:
                maps.append(this_ranges)

            this_ranges = Ranges()

            continue

        # logging.info(line)

        if line[0].isdigit():
            params = list(map(int, line.split()))
            this_ranges.add_range(Range(params[1], params[0], params[2]))

    maps.append(this_ranges)
    maps.reverse()

    # for location in range(40, 100):
    #     seed = functools.reduce(lambda seed, ranges: ranges.evaluate(seed), maps, location)
    #     print(location, seed)

    seed_ranges = list(zip(seeds[::2], seeds[1::2]))

    location = 9000000
    while True:
        seed = functools.reduce(lambda seed, ranges: ranges.evaluate(seed), maps, location)

        for start, length in seed_ranges:
            if start <= seed < (start + length):
                part_two = location
                break

        if part_two != 0:
            break

        location += 1
        if location % 100000 == 0:
            print(location)

    return part_one, part_two
