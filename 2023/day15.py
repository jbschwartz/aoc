import dataclasses
import enum
import logging
from functools import reduce
from typing import TextIO


class Operation(enum.Enum):
    DASH = "-"
    EQUALS = "="


@dataclasses.dataclass
class Lens:
    label: str
    focal_length: int = None

    def __str__(self) -> str:
        return f"{self.label} {self.focal_length}"

    def focal_power(self, box_index: int, slot_index: int) -> int:
        """Compute the focal power of the lens."""
        return int(self.focal_length) * (box_index + 1) * (slot_index + 1)


@dataclasses.dataclass
class Boxes:
    boxes: dict = dataclasses.field(default_factory=dict)

    def __str__(self) -> str:
        string = ""
        for box_index, lenses in self.boxes.items():
            if len(lenses) == 0:
                continue

            lens_string = " ".join(f"[{lens}]" for lens in lenses)
            string += f"Box {box_index}: {lens_string}\n"

        string += "\n"
        return string

    def execute(self, lens: Lens, operation: Operation) -> None:
        """Execute the operation for the given lens."""
        box_index = hash_string(lens.label)

        if box_index not in self.boxes:
            self.boxes[box_index] = [lens]
            return

        # Remove the box from the list of boxes.
        if operation is Operation.DASH:
            self.boxes[box_index] = [
                current_lens
                for current_lens in self.boxes[box_index]
                if current_lens.label != lens.label
            ]
        else:
            # Replace the focal length if it exists, otherwise add it to the end.
            for current_lens in self.boxes[box_index]:
                if current_lens.label == lens.label:
                    current_lens.focal_length = lens.focal_length
                    break
            else:
                self.boxes[box_index].append(lens)

    def focusing_power(self) -> int:
        """Get the focusing power for all lenses in the boxes."""
        power = 0
        for box_index, lenses in self.boxes.items():
            for slot_index, lens in enumerate(lenses):
                power += lens.focal_power(box_index, slot_index)

        return power


def hash_string(string: str) -> int:
    """Return the hash of the provided string."""
    return reduce(lambda value, char: ((value + ord(char)) * 17) % 256, string, 0)


def parse_step(step: str) -> tuple[Lens, Operation]:
    """Parse each step into a lens and operation."""
    if "=" in step:
        return (Lens(*step.split("=")), Operation.EQUALS)

    return (Lens(step[:-1]), Operation.DASH)


def parse_steps(file: TextIO) -> list[str]:
    """Return a list of steps from the input."""
    return file.readline().strip().split(",")


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    return sum(hash_string(step) for step in parse_steps(file))


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    boxes = Boxes()
    for step in parse_steps(file):
        boxes.execute(*parse_step(step))

    logging.info(boxes)

    return boxes.focusing_power()
