import logging
from typing import TextIO, Tuple

# pylint: disable=too-few-public-methods
class CRT:
    """The CRT display which is driven by the Machine."""

    def __init__(self):
        self.cycle: int = 0
        self.width: int = 40
        self.row: str = ""

    def draw(self, register_value: int) -> None:
        """Draw a pixel on the CRT at the current horizontal position given the register value."""
        horizontal_position = self.cycle % self.width

        if horizontal_position == 0 and self.row:
            print(self.row)
            self.row = ""

        if abs(register_value - horizontal_position) <= 1:
            self.row += "#"
        else:
            self.row += " "

        self.cycle += 1


class Machine:
    """The machine which keeps track of a register value x."""

    def __init__(self, signals) -> None:
        self.signals = signals
        self.cycle = 1
        self.x = 1
        self.is_busy = 0
        self.callback = None
        self.strength = 0

        self.display = CRT()

    def __str__(self) -> str:
        return f"{self.cycle}: {self.x} ({self.is_busy})"

    def process(self, command, *args):
        """Handle a command from the program."""
        function = getattr(self, f"_{command}")

        function(*args)

    def tick_until_idle(self):
        """Advance the machine cycle by cycle until it is ready for a new command."""
        self._tick()
        while self.is_busy > 0:
            self._tick()

    def _addx(self, value, *_args):
        """Add the value to the x register."""
        self.is_busy = 2

        def callback():
            self.x += int(value)

        self.callback = callback

    def _compute_strength(self):
        """Compute the signal strength."""
        if self.cycle in self.signals:
            self.strength += self.cycle * self.x

    def _noop(self, *_args):
        """Do nothing this cycle."""
        self.callback = None

    def _tick(self):
        """Advance the machine by one cycle."""
        logging.debug(self)

        self.display.draw(self.x)

        self._compute_strength()

        self.cycle += 1
        self.is_busy = max(0, self.is_busy - 1)

        if self.is_busy == 0 and self.callback is not None:
            self.callback()


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    machine = Machine([20, 60, 100, 140, 180, 220])

    commands = [line.strip().split(" ") for line in file]

    for command in commands:
        logging.debug(command)
        machine.process(command[0], *command[1:])

        machine.tick_until_idle()

    machine.tick_until_idle()

    part_one = machine.strength

    return part_one, part_two
