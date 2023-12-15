import logging
from typing import TextIO

# The total number of iterations in part two.
TOTAL_SPIN_CYCLES = 1000000000


class Rocks:
    def __init__(self, lines: list[list[str]]) -> None:
        self.lines = lines

    def __str__(self) -> str:
        """Return the text representation of the rocks at the current iteration."""
        lines = ["".join(line) for line in self.lines]
        return "\n".join(lines)

    @property
    def columns(self) -> list[list[str]]:
        """Return the columns of the rocks."""
        return [[line[index] for line in self.lines] for index in range(self.line_length)]

    @property
    def line_length(self) -> int:
        """Return the row length (number of columns) of the rocks."""
        return len(self.lines[0])

    @property
    def number_of_rows(self) -> int:
        """Return the column length (number of rows) of the rocks."""
        return len(self.lines)

    def load(self) -> int:
        """Roll rocks to the west."""
        load = 0
        for row_index, line in enumerate(self.lines):
            for char in line:
                if char == "O":
                    load += self.number_of_rows - row_index

        return load

    def roll_east(self) -> None:
        """Roll rocks to the east."""
        for index, line in enumerate(self.lines):
            reverse = line[::-1]
            self.lines[index] = self._roll_line_west(reverse)[::-1]

    def roll_north(self) -> None:
        """Roll rocks to the north."""
        for index, line in enumerate(self.columns):
            self._set_column(index, self._roll_line_west(line))

    def roll_south(self) -> None:
        """Roll rocks to the south."""
        for index, line in enumerate(self.columns):
            reverse = line[::-1]
            self._set_column(index, self._roll_line_west(reverse)[::-1])

    def roll_west(self) -> None:
        """Roll rocks to the west."""
        for index, line in enumerate(self.lines):
            self.lines[index] = self._roll_line_west(line)

    def spin_cycle(self) -> None:
        """Perform a spin cycle."""
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()

    def _set_column(self, column_index: int, line: list[list[str]]) -> None:
        """Set the column to the provided line."""
        for row_index, char in enumerate(line):
            self.lines[row_index][column_index] = char

    def _roll_line_west(self, line: list[str]) -> list[str]:
        """Roll the provided line to the west.

        This is the canonical direction used by all other directions.
        """
        new_line = ["."] * len(line)

        current_index = 0
        for index, char in enumerate(line):
            if char == "O":
                new_line[current_index] = "O"
                current_index += 1

            elif char == "#":
                new_line[index] = "#"
                current_index = index + 1

        return new_line


def parse_rocks(file: TextIO) -> Rocks:
    """Parse the input into Rocks."""
    lines = []

    for line in file:
        line = line.strip()
        lines.append(list(line))

    return Rocks(lines)


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    rocks = parse_rocks(file)
    rocks.roll_north()

    return rocks.load()


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    cache = {}

    rocks = parse_rocks(file)

    index = 0
    while True:
        rocks.spin_cycle()
        index += 1

        string = str(rocks)

        if string in cache:
            last_index = cache[string]
            cycle_length = index - last_index
            remaining = (TOTAL_SPIN_CYCLES - index) % cycle_length

            logging.info(f"Cache hit at index {index}: last saw at index {last_index}")
            logging.info(f"Cycle length: {cycle_length}")
            logging.info(f"Remaining: {remaining}")

            for index in range(remaining):
                rocks.spin_cycle()

            return rocks.load()
        else:
            cache[string] = index
