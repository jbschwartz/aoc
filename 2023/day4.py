import logging
from typing import TextIO, Tuple


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    # for line in file:
    #     line = line.strip()
    #     card, numbers = line.split(":")

    #     id = int(card.strip().split(" ")[-1])

    #     winning_numbers, our_numbers = map(
    #         lambda numbers: set(n for n in numbers.strip().split(" ") if n != ""),
    #         numbers.strip().split("|"),
    #     )

    #     num_matches = len(winning_numbers.intersection(our_numbers))

    #     if num_matches > 0:
    #         part_one += 2 ** (num_matches - 1)

    copies = [0]

    for id, line in enumerate(file, 1):
        _, numbers = line.strip().split(":")

        winning_numbers, our_numbers = map(
            lambda numbers: set(n for n in numbers.strip().split(" ") if n != ""),
            numbers.strip().split("|"),
        )

        num_matches = len(winning_numbers.intersection(our_numbers))

        if len(copies) <= id:
            copies.append(1)
        else:
            copies[id] += 1

        for i in range(num_matches):
            try:
                copies[id + i + 1] += copies[id]
            except IndexError:
                copies.append(copies[id])

    part_two = sum(copies)

    return part_one, part_two
