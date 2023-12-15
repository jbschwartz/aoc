from typing import Optional, TextIO, Tuple


class Pattern:
    # The puzzle defines horizontal mirrors as being worth 100 more than vertical mirrors.
    HORIZONTAL_MULTIPLIER = 100

    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    @property
    def columns(self) -> list[str]:
        """Return the columns of the pattern as a list of strings."""
        return ["".join(line[index] for line in self.lines) for index in range(self.line_length)]

    @property
    def line_length(self) -> int:
        """Return the row length (number of columns) of the pattern."""
        return len(self.lines[0])

    @property
    def pattern_length(self) -> int:
        """Return the column length (number of rows) of the pattern."""
        return len(self.lines)

    def get_mirror_result(self) -> int:
        """Compute the value of the mirror in the pattern."""
        if index := self._mirror_index(self.lines):
            return index

        return self.HORIZONTAL_MULTIPLIER * self._mirror_index(self.columns)

    def get_smudge_result(self) -> int:
        """Compute the value of the pattern after correcting the smudge."""
        if index := self._find_smudge(self.lines, self.pattern_length):
            return index

        return self.HORIZONTAL_MULTIPLIER * self._find_smudge(self.columns, self.line_length)

    def _find_smudge(self, lines: list[str], length: int) -> int:
        """Return the mirror line index which is one row/column short of being a mirror."""
        # Count the occurances of each index.
        occurance_count = {}
        for index_set in self._get_index_sets(lines):
            for index in index_set:
                if index in occurance_count:
                    occurance_count[index] += 1
                else:
                    occurance_count[index] = 1

        # Then find the index which is exactly one fewer than the length.
        for index, occurances in occurance_count.items():
            if occurances == (length - 1):
                return index

    def _get_index_sets(self, lines: list[str]) -> list[set[int]]:
        """Return a list of sets containing mirror indexes for each line."""
        return [self._get_mirrors(line) for line in lines]

    def _get_mirrors(self, line: str) -> set[int]:
        """Return a set of valid mirror indices for the provided line."""
        mirrors = []
        for mirror_index in range(1, len(line)):
            left_side = line[:mirror_index]
            right_side = line[mirror_index : 2 * mirror_index]

            if left_side.endswith(right_side[::-1]):
                mirrors.append(mirror_index)

        return set(mirrors)

    def _mirror_index(self, lines: list[str]) -> Optional[int]:
        """Return the mirror location for the given lines. Return None if one does not exist."""
        # Find the index which is shared on every single line (if one exists).
        common_index = set.intersection(*self._get_index_sets(lines))

        assert len(common_index) <= 1

        if len(common_index) == 0:
            return None

        return common_index.pop()


def parse_patterns(file: TextIO) -> list[Pattern]:
    """Return a list of Patterns from the given input file."""
    patterns = []
    lines = []

    while line := file.readline():
        line = line.strip()

        if line:
            lines.append(line)
        else:
            patterns.append(Pattern(lines))
            lines = []

    patterns.append(Pattern(lines))

    return patterns


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    return sum(pattern.get_mirror_result() for pattern in parse_patterns(file))


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    return sum(pattern.get_smudge_result() for pattern in parse_patterns(file))
