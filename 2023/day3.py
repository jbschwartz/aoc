import dataclasses
import logging
from typing import TextIO, Tuple


@dataclasses.dataclass
class Part:
    row: int
    start: int
    value: int
    end: int = 0
    is_part: bool = False

    def is_adjacent(self, symbol) -> bool:
        return (self.start - 1) <= symbol.start <= (self.end + 1) and (
            self.row - 1
        ) <= symbol.row <= (self.row + 1)


@dataclasses.dataclass
class Symbol:
    row: int
    start: int
    char: str
    ratio: int = 1


def get_parts_symbols(file) -> tuple[list[Part], list[Symbol]]:
    """Get a list of parts and symbols from the input."""
    parts = []
    symbols = []
    for row_index, line in enumerate(file):
        line = line.strip()

        in_part = False

        for column_index, char in enumerate(line):
            if char.isdigit():
                if in_part:
                    parts[-1].value *= 10
                    parts[-1].value += int(char)
                else:
                    parts.append(Part(row_index, column_index, int(char)))

                in_part = True
            else:
                if char != ".":
                    symbols.append(Symbol(row_index, column_index, char))

                if in_part:
                    parts[-1].end = column_index - 1

                in_part = False

        if parts[-1].end == 0:
            parts[-1].end = column_index - 1

    return parts, symbols


def one(file: TextIO) -> Tuple[int, int]:
    """Run the first part for this day."""
    result = 0

    parts, symbols = get_parts_symbols(file)

    for part in parts:
        for symbol in symbols:
            if part.is_adjacent(symbol):
                part.is_part = True
                result += part.value
                break

    return result


def two(file: TextIO) -> Tuple[int, int]:
    """Run the second part for this day."""
    result = 0

    parts, symbols = get_parts_symbols(file)

    for symbol in symbols:
        if symbol.char != "*":
            continue

        num_adjacent = 0
        for part in parts:
            if part.is_adjacent(symbol):
                num_adjacent += 1
                symbol.ratio *= part.value

            if num_adjacent > 2:
                break

        if num_adjacent == 2:
            result += symbol.ratio

    return result
