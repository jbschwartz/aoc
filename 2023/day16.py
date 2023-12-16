import dataclasses
import enum
import logging
from typing import Optional, TextIO


class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


class CellType(enum.Enum):
    MIRROR_FORWARD = "/"
    MIRROR_BACKWARD = "\\"
    SPLIT_VERTICAL = "|"
    SPLIT_HORIZONTAL = "-"
    EMPTY = "."


@dataclasses.dataclass
class Beam:
    position: tuple[int, int] = (0, 0)
    direction: Direction = Direction.EAST
    is_done: bool = False

    def __str__(self) -> int:
        """Return a string representation of the beam in its current position."""
        return f"{self.direction.name}{self.position}"

    def advance(self, new_direction: Direction) -> None:
        """Advance the head of the beam in the provided direction."""
        self.direction = new_direction
        self.position = (
            self.position[0] + self.direction.value[0],
            self.position[1] + self.direction.value[1],
        )


@dataclasses.dataclass
class Cell:
    type: CellType
    energized: bool = False


@dataclasses.dataclass
class Grid:
    cells: list[Cell]
    cache: dict = dataclasses.field(default_factory=dict)

    @classmethod
    def from_input(cls, file: TextIO) -> "Grid":
        """Create a Grid from the given input file."""
        lines = []
        for line in file:
            lines.append([Cell(CellType(char)) for char in line.strip()])

        return cls(lines)

    def __str__(self) -> str:
        string = ""
        for row in self.cells:
            for cell in row:
                string += "#" if cell.energized else "."
            string += "\n"

        return string

    @property
    def num_columns(self) -> int:
        """Return the number of columns in the grid."""
        return len(self.cells)

    @property
    def num_rows(self) -> int:
        """Return the number of rows in the grid."""
        return len(self.cells)

    @property
    def num_energized(self) -> int:
        total = 0
        for row in self.cells:
            for cell in row:
                total += 1 if cell.energized else 0

        return total

    def perimeter_beams(self) -> list[Beam]:
        """Return a list of all possible perimeter beams."""
        perimeter_beams = []

        for index in range(self.num_rows):
            perimeter_beams.append(Beam((0, index), Direction.EAST))
            perimeter_beams.append(Beam((self.num_columns - 1, index), Direction.WEST))

        for index in range(self.num_columns):
            perimeter_beams.append(Beam((index, 0), Direction.SOUTH))
            perimeter_beams.append(Beam((index, self.num_rows - 1), Direction.NORTH))

        return perimeter_beams

    def reset(self) -> None:
        """Reset the grid to start over."""
        for row in self.cells:
            for cell in row:
                cell.energized = False

        self.cache = {}

    def trace_all(self, start_beam: Beam) -> None:
        """Trace all beams from the provided start beam."""
        beams = [start_beam]
        while True:
            new_beams = []
            for beam in beams:
                if beam.is_done:
                    continue

                if new_beam := self._trace(beam):
                    new_beams.append(new_beam)

            beams.extend(new_beams)
            if all(beam.is_done for beam in beams):
                break

    def _cell_at(self, position: tuple[int, int]) -> Optional[Cell]:
        """Return the cell at the provided position or None if off the grid."""
        try:
            if position[0] < 0 or position[1] < 0:
                return None

            return self.cells[position[1]][position[0]]
        except IndexError:
            return None

    def _next_directions(
        self, direction: Direction, cell_type: CellType
    ) -> tuple[Direction, Optional[Direction]]:
        """Get the next beam directions based on the input direction and cell type.

        Splitters will return two different directions.
        """
        match cell_type:
            case CellType.MIRROR_FORWARD:
                match direction:
                    case Direction.NORTH:
                        return (Direction.EAST, None)
                    case Direction.SOUTH:
                        return (Direction.WEST, None)
                    case Direction.EAST:
                        return (Direction.NORTH, None)
                    case Direction.WEST:
                        return (Direction.SOUTH, None)

            case CellType.MIRROR_BACKWARD:
                match direction:
                    case Direction.NORTH:
                        return (Direction.WEST, None)
                    case Direction.SOUTH:
                        return (Direction.EAST, None)
                    case Direction.EAST:
                        return (Direction.SOUTH, None)
                    case Direction.WEST:
                        return (Direction.NORTH, None)

            case CellType.SPLIT_VERTICAL:
                match direction:
                    case Direction.NORTH | Direction.SOUTH:
                        return (direction, None)
                    case Direction.EAST | Direction.WEST:
                        return (Direction.NORTH, Direction.SOUTH)

            case CellType.SPLIT_HORIZONTAL:
                match direction:
                    case Direction.EAST | Direction.WEST:
                        return (direction, None)
                    case Direction.NORTH | Direction.SOUTH:
                        return (Direction.EAST, Direction.WEST)

            case CellType.EMPTY:
                return (direction, None)

    def _trace(self, beam: Beam) -> Optional[Beam]:
        """Trace the beam forward one cell. Return any new beams caused by splitters."""
        cell = self._cell_at(beam.position)

        if not cell or str(beam) in self.cache:
            beam.is_done = True
            return None

        cell.energized = True
        self.cache[str(beam)] = True

        next_direction, split_direction = self._next_directions(beam.direction, cell.type)

        split_beam = Beam(beam.position, split_direction) if split_direction else None

        beam.advance(next_direction)

        return split_beam


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    grid = Grid.from_input(file)

    grid.trace_all(Beam())

    logging.info(grid)

    return grid.num_energized


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    grid = Grid.from_input(file)

    # There is almost definitely a way to memoize this; at every cell you can cache the number of
    # energized cells which follow (after tracing it once). This would drastically reduce the number
    # of beam traces required.
    maximum = -1
    for beam in grid.perimeter_beams():
        grid.trace_all(beam)

        maximum = max(maximum, grid.num_energized)

        grid.reset()

    return maximum
