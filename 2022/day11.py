import logging
import math
from typing import TextIO, Tuple, List, Callable


class Monkey:
    """The main character in Day 11."""

    def __init__(
        self,
        index: int,
        items: List[int],
        operation: Callable,
        divisor: int,
        pass_true: int,
        pass_false: int,
    ):
        self.index = index
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.pass_true = pass_true
        self.pass_false = pass_false

        self.inspections: int = 0

    @classmethod
    def from_spec(cls, lines: str) -> "Monkey":
        """Return a Monkey from a input specification lines."""
        index = int(lines[0].split(" ")[-1].rstrip(":"))
        items = list(map(int, lines[1].split(":")[-1].split(", ")))

        operation_strings = lines[2].split(" ")[-2:]

        def operation(value: int) -> int:
            if operation_strings[1] == "old":
                operand = value
            else:
                operand = int(operation_strings[1])

            if operation_strings[0] == "+":
                return value + operand

            if operation_strings[0] == "*":
                return value * operand

            raise NotImplementedError(f"Unknown operation {operation_strings[0]}")

        divisor = int(lines[3].split(" ")[-1])
        pass_true = int(lines[4].split(" ")[-1])
        pass_false = int(lines[5].split(" ")[-1])

        logging.debug(f"{index}, {items}, {divisor}, {pass_true}, {pass_false}")

        return cls(index, items, operation, divisor, pass_true, pass_false)

    def inspect(self, worry_mitigation, least_common_mult) -> List[Tuple[int, int]]:
        """Compute worry levels and then return a list of destination-item pairs."""
        passes = []
        for item in self.items:
            logging.debug(f"Monkey {self.index} inspecting {item}")
            self.inspections += 1

            # Use the least common multiple to bound the worry levels. Otherwise these numbers get
            # very large!
            new_worry_level = math.floor(
                (self.operation(item) % least_common_mult) / worry_mitigation
            )

            if new_worry_level % self.divisor == 0:
                destination = self.pass_true
            else:
                destination = self.pass_false

            passes.append((destination, new_worry_level))
            logging.debug(f"> Passing {new_worry_level} to {destination}")

        self.items = []

        return passes


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    monkey_specs = file.read().split("\n\n")

    results = []
    for trials, mitigation in [(20, 3), (10000, 1)]:
        monkies = [Monkey.from_spec(spec.split("\n")) for spec in monkey_specs]

        # Making the assumption that all the divisors are unique prime numbers. Otherwise this is
        # still a common multiple but not necessarily the least.
        least_common_mult = 1
        for monkey in monkies:
            least_common_mult *= monkey.divisor

        for _ in range(trials):
            for monkey in monkies:
                for destination, item in monkey.inspect(mitigation, least_common_mult):
                    monkies[destination].items.append(item)

        first, second = sorted(monkies, key=lambda monkey: monkey.inspections, reverse=True)[0:2]

        results.append(first.inspections * second.inspections)

    return results
