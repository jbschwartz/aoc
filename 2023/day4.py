from typing import TextIO, Tuple


def num_matches(line: str) -> int:
    """Return the number of matches for the given line."""
    card, numbers = line.strip().split(":")

    # Create sets to perform an intersection.
    winning_numbers, our_numbers = map(
        lambda numbers: set(n for n in numbers.strip().split()),
        numbers.strip().split("|"),
    )

    return len(winning_numbers.intersection(our_numbers))


def one(file: TextIO) -> Tuple[int, int]:
    """Run the first part for this day."""
    result = 0

    for line in file:
        matches = num_matches(line)

        if matches > 0:
            result += 2 ** (matches - 1)

    return result


def two(file: TextIO) -> Tuple[int, int]:
    """Run the second part for this day."""
    copies = [0]

    for id, line in enumerate(file, 1):
        try:
            copies[id] += 1
        except IndexError:
            # Create an element to keep track of the number of copies of this particular card.
            copies.append(1)

        for i in range(1, num_matches(line) + 1):
            # Add a new copy for each card from this cards winners.
            try:
                copies[id + i] += copies[id]
            except IndexError:
                copies.append(copies[id])

    return sum(copies)
