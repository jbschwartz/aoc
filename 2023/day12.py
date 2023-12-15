from typing import TextIO, Tuple


class Record:
    def __init__(self, string: str, expected_groups: list[int]):
        # Removing functional springs at the end of the record has no effect.
        self.string = string.strip(".")
        self.expected_groups = expected_groups

        self.hash = self.string + str(len(self.expected_groups))

    @classmethod
    def from_line(cls, line: str) -> "Record":
        """Create a Record from a line of input."""
        string, groups = line.strip().split()

        string = string.strip(".")
        groups = list(map(int, groups.split(",")))

        return cls(string, groups)

    def __str__(self) -> str:
        groups = ",".join(map(str, self.expected_groups))
        return f"{self.string} {groups}"

    @property
    def complete(self) -> bool:
        """Return True if there are no more unknowns in the record."""
        return "?" not in self.string

    @property
    def groups(self) -> list[int]:
        """Return the length of each group of contiguous damaged springs."""
        return list(map(len, filter(lambda group: group, self.string.split("."))))

    @property
    def starts_with_unknown(self) -> bool:
        """Return True if the first character is "?"."""
        return "?" == self.string[0]

    @property
    def valid(self) -> bool:
        """Return True if the actual damaged groups match the expected and the record is valid."""
        assert (
            self.complete
        ), "Computing this property does not make sense unless the record is complete."

        return self.groups == self.expected_groups

    def can_match_first_group(self) -> bool:
        """Return True if the beginning of the record can match the first group."""
        # There are no groups left to match so we shouldn't continue down this path.
        if len(self.expected_groups) == 0:
            return False

        first_group_size = self.expected_groups[0]

        # The group is larger than there are characters remaining.
        if len(self.string) < first_group_size:
            return False

        # In order to match, all of the next n springs (where n is the group size) must be "#" or
        # "?", otherwise the actual group will be smaller than expected.
        if "." in self.string[:first_group_size]:
            return False

        # If there are no more characters, we must have a match.
        # Check this first so we do not go beyond the end of the string on the next if statement.
        if len(self.string) == first_group_size:
            return True

        # If the spring following the group is damaged, the group ends up being larger than we
        # expected (by at least 1) so we cannot match.
        return self.string[first_group_size] != "#"

    def match_first_group(self) -> "Record":
        """Return a new record with the first group already matched."""
        return Record(self.string[self.expected_groups[0] + 1 :], self.expected_groups[1:])

    def unknown_is_operational(self) -> "Record":
        """Return a new record with the first unknown operational."""
        return Record(self.string[1:], self.expected_groups)


def compute_arrangements(record: Record, cache: dict = None) -> int:
    # If the record is complete, there are no further possibilities to uncover.
    if record.complete:
        return 1 if record.valid else 0

    if cache is None:
        cache = {}

    # See if this substring has already been computed before. Include the number of groups since
    # how we got to this substring matters (e.g., did we have more or less damaged springs prior
    # to this).
    if record.hash in cache:
        return cache[record.hash]

    # There are two possibilites for every record:
    #   1. The next group can matched at the beginning of the current record by assuming the
    #      unknowns are damaged.
    #   2. The next unknown is assumed to be functional.
    #
    # Recurse into both possibilities.

    arrangements = 0
    if record.can_match_first_group():
        arrangements += compute_arrangements(record.match_first_group(), cache)

    if record.starts_with_unknown:
        arrangements += compute_arrangements(record.unknown_is_operational(), cache)

    # Cache this substring so that other branches may benefit from it.
    cache[record.hash] = arrangements

    return arrangements


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    result = 0

    for line in file:
        record = Record.from_line(line)
        result += compute_arrangements(record)

    return result


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    result = 0

    for line in file:
        string, groups = line.strip().split()

        string = "?".join([string] * 5)
        groups = ",".join([groups] * 5)

        record = Record.from_line(f"{string} {groups}")
        result += compute_arrangements(record)

    return result
