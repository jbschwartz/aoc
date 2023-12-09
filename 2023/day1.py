import logging
from typing import TextIO, Tuple


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    # for line in file:
    #     first_digit = None
    #     last_digit = None

    #     for char in line.strip():
    #         if char.isnumeric():
    #             last_digit = int(char)
    #             if not first_digit:
    #                 first_digit = int(char) * 10

    #     part_one += first_digit + last_digit

    # needles = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    # for line in file:
    #     line = line.strip()
    #     logging.info(line)
    #     min_positions = [None] * len(needles)
    #     max_positions = [None] * len(needles)

    #     for value, needle in enumerate(needles):
    #         min_positions[value] = line.find(needle)
    #         max_positions[value] = line.rfind(needle)

    #     try:
    #         min_index = min_positions.index(min(p for p in min_positions if p >= 0))
    #         line = line.replace(needles[min_index], str(min_index))
    #     except ValueError:
    #         pass

    #     max_index = max_positions.index(max(max_positions))
    #     line = line.replace(needles[max_index], str(max_index))

    #     first_digit = None
    #     last_digit = None

    #     for char in line.strip():
    #         if char.isnumeric():
    #             last_digit = int(char)
    #             if not first_digit:
    #                 first_digit = int(char) * 10
    #     logging.info(line)
    #     logging.info(first_digit + last_digit)
    #     input()
    #     part_two += first_digit + last_digit

    needles = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    for line in file:
        line = line.strip()
        logging.info(line)

        while True:
            min_positions = [None] * len(needles)

            for value, needle in enumerate(needles):
                min_positions[value] = line.find(needle)

            try:
                min_index = min_positions.index(min(p for p in min_positions if p >= 0))
            except ValueError:
                break

            line = line.replace(
                needles[min_index],
                needles[min_index][0] + str(min_index) + needles[min_index][-1],
                1,
            )

        logging.info(line)

        first_digit = None
        last_digit = None

        for char in line.strip():
            if char.isnumeric():
                last_digit = int(char)
                if not first_digit:
                    first_digit = int(char) * 10

        logging.info(first_digit + last_digit)
        part_two += first_digit + last_digit

    return part_one, part_two
