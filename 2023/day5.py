import dataclasses
import functools
from typing import TextIO, Tuple


@dataclasses.dataclass
class Range:
    start: int
    length: int

    def __str__(self) -> str:
        return f"[{self.start}, {self.end}]"

    @classmethod
    def from_endpoints(cls, start: int, end: int) -> "Range":
        length = end - start + 1
        return cls(start, length)

    def __lt__(self, other: "Range") -> bool:
        return self.start < other.start

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def intersects(self, other: "Range") -> bool:
        """Return True if the ranges are intersecting."""
        return self.start <= other.end and self.end >= other.start

    def superset_of(self, other: "Range") -> bool:
        """Return True if this range is a superset of the other range."""
        return self.start <= other.start and self.end >= other.end

    def split_intersections(self, other: "Range") -> tuple["Range", list["Range"]]:
        """Return intersection the intersection with other and a list of split ranges."""
        if not self.intersects(other):
            return (None, [other])

        if self.superset_of(other):
            return (other, [])

        if other.superset_of(self):
            if other.start == self.start:
                return (
                    Range(self.start, self.length),
                    [Range.from_endpoints(self.end + 1, other.end)],
                )

            elif other.end == self.end:
                return (
                    Range(self.start, self.length),
                    [Range.from_endpoints(other.start, self.start - 1)],
                )

            else:
                return (
                    Range(self.start, self.length),
                    [
                        Range.from_endpoints(other.start, self.start - 1),
                        Range.from_endpoints(self.end + 1, other.end),
                    ],
                )

        if self.start <= other.start:
            return (
                Range.from_endpoints(other.start, self.end),
                [Range.from_endpoints(self.end + 1, other.end)],
            )
        else:
            return (
                Range.from_endpoints(self.start, other.end),
                [Range.from_endpoints(other.start, self.start - 1)],
            )


@dataclasses.dataclass
class RangeMap:
    destination: Range
    source: Range

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination}"

    def evaluate(self, source: int) -> int | None:
        if self.source.start <= source <= self.source.end:
            return self.destination.start + (source - self.source.start)

        return None

    def evaluate_range(self, input_range: "Range") -> "Range":
        assert self.source.superset_of(input_range)

        return Range.from_endpoints(
            self.evaluate(input_range.start), self.evaluate(input_range.end)
        )

    def split_evaluate(self, input_range: "Range") -> tuple[Range, list[Range]]:
        intersecting, others = self.source.split_intersections(input_range)

        if not intersecting:
            return None, others

        return self.evaluate_range(intersecting), others


class Mapping:
    def __init__(self, name: str, range_maps: list[RangeMap]) -> None:
        self.name = name
        self.range_maps = range_maps

    @classmethod
    def from_lines(cls, name: str, lines: list[str]) -> "Mapping":
        range_maps = []

        for line in lines:
            destination_start, source_start, length = list(map(int, line.split()))

            destination = Range(destination_start, length)
            source = Range(source_start, length)

            range_maps.append(RangeMap(destination, source))

        return cls(name, range_maps)

    def __str__(self) -> str:
        return f"{self.name}: " + ", ".join(map(str, self.range_maps))

    def evaluate(self, source: int) -> int:
        for range in self.range_maps:
            if value := range.evaluate(source):
                return value

        return source

    def evaluate_range(self, source_range: "Range") -> list["Range"]:
        ranges_to_evaluate = [source_range]
        output_ranges = []

        for range_map in self.range_maps:
            new_ranges = []

            for input_range in ranges_to_evaluate:
                evaluated, not_evaluated = range_map.split_evaluate(input_range)

                if evaluated:
                    output_ranges.append(evaluated)

                new_ranges.extend(not_evaluated)

            ranges_to_evaluate = new_ranges

        output_ranges.extend(ranges_to_evaluate)

        return output_ranges


def parse(file: TextIO) -> tuple[list[int], list[Mapping]]:
    """Return the list of seeds and the mappings from the input file."""
    seeds = list(map(int, file.readline().strip().split()[1:]))

    mappings = []
    while line := file.readline():
        line = line.strip()

        if line.endswith("map:"):
            name = line.split()[0]

            lines = []
            while line := file.readline().strip():
                lines.append(line)

            mappings.append(Mapping.from_lines(name, lines))

    return seeds, mappings


def interpret_seeds_as_ranges(seeds: list[int]) -> list[Range]:
    return [Range(start, length) for start, length in zip(seeds[::2], seeds[1::2])]


def one(file: TextIO) -> Tuple[int, int]:
    """Run the first part for this day."""
    seeds, mappings = parse(file)

    return min(
        functools.reduce(lambda seed, mapping: mapping.evaluate(seed), mappings, seed)
        for seed in seeds
    )


def two(file: TextIO) -> Tuple[int, int]:
    """Run the second part for this day."""
    seeds, mappings = parse(file)

    ranges = interpret_seeds_as_ranges(seeds)

    for mapping in mappings:
        ranges = [new_range for range in ranges for new_range in mapping.evaluate_range(range)]

    return min(ranges).start
