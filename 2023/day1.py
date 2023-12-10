from typing import TextIO, Tuple


def get_first_and_last_digit(line: str) -> tuple[int, int]:
    """Return the first and last digit in the line."""
    first_digit = None
    last_digit = None

    for char in line.strip():
        try:
            value = int(char)
        except ValueError:
            continue

        if not first_digit:
            first_digit = value

        last_digit = value

    return first_digit, last_digit


def get_line_value(line: str) -> int:
    """Get the value for the given line."""
    first_digit, last_digit = get_first_and_last_digit(line)
    return 10 * first_digit + last_digit


def replacement(string: str, value: int) -> str:
    """Return the replacement value for the given string."""
    # Replace the number with the actual digit but include the first and last letter so that
    # chained values are correctly intepreted (e.g., "oneight" => "o1e8t" => 18)
    return string[0] + str(value) + string[-1]


def one(file: TextIO) -> Tuple[int, int]:
    """Run the first part for this day."""
    return sum(get_line_value(line) for line in file)


def two(file: TextIO) -> Tuple[int, int]:
    """Run the second part for this day."""
    result = 0

    needles = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    for line in file:
        line = line.strip()

        for value, needle in enumerate(needles):
            line = line.replace(needle, replacement(needle, value))

        result += get_line_value(line)

    return result
