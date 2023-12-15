import dataclasses
from typing import TextIO, Tuple


@dataclasses.dataclass
class Galaxy:
    index: int
    row: int
    column: int

    def distance_to(self, other: "Galaxy") -> int:
        """Return the Manhattan norm distance between this galaxy and another."""
        return abs(other.row - self.row) + abs(other.column - self.column)


def compute_distances_between_pairs(galaxies: list[Galaxy]) -> list[int]:
    """Compute a list of distances between all galaxy pairs."""
    distances = []
    for i, first in enumerate(galaxies):
        for second in galaxies[i + 1 :]:
            distances.append(first.distance_to(second))

    return distances


def parse(file: TextIO, galaxy_spacing: int = 1) -> list[Galaxy]:
    """Return a list of galaxies from the input file with the appropriate space added."""
    column_has_galaxy = None

    galaxies = []

    num_empty_rows = 0
    for row_index, line in enumerate(file):
        line = line.strip()

        # Initialize the array keeping track of whether or not a column has a galaxy.
        if row_index == 0:
            column_has_galaxy = [False] * len(line)

        row_has_galaxy = False
        for column_index, char in enumerate(line):
            if char == "#":
                row_has_galaxy = True
                column_has_galaxy[column_index] = True
                galaxies.append(
                    Galaxy(
                        len(galaxies) + 1, row_index + num_empty_rows * galaxy_spacing, column_index
                    )
                )

        if not row_has_galaxy:
            num_empty_rows += 1

    blank_columns = [index for index, has_galaxy in enumerate(column_has_galaxy) if not has_galaxy]

    blank_columns.reverse()

    for column_index in blank_columns:
        for galaxy in galaxies:
            if galaxy.column > column_index:
                galaxy.column += galaxy_spacing

    return galaxies


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    galaxies = parse(file)

    return sum(compute_distances_between_pairs(galaxies))


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    galaxies = parse(file, 999999)

    return sum(compute_distances_between_pairs(galaxies))
