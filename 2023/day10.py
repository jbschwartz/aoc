import dataclasses
import enum
from functools import cached_property
from typing import Optional, TextIO, Tuple


class Direction(enum.Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTH_EAST = (1, -1)


class ConnectedPipes(enum.Enum):
    NORTH = "|7F"
    SOUTH = "|LJ"
    EAST = "-J7"
    WEST = "-FL"


@dataclasses.dataclass
class Cell:
    """A single cell in the map."""

    indices: tuple[int, int]
    pipe: str
    is_loop: bool = False
    direction_value: int = 0
    enclosed: bool = False

    def connected_to(self, other: "Cell", direction: Direction) -> bool:
        """Return True if this cell is connected to the other."""
        return other.pipe in ConnectedPipes[direction.name].value or other.pipe == "S"

    def valid_directions(self) -> list[Direction]:
        """Return the valid directions from this cell."""
        match self.pipe:
            case "S":
                return [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
            case "|":
                return [Direction.NORTH, Direction.SOUTH]
            case "7":
                return [Direction.WEST, Direction.SOUTH]
            case "J":
                return [Direction.WEST, Direction.NORTH]
            case "F":
                return [Direction.EAST, Direction.SOUTH]
            case "L":
                return [Direction.EAST, Direction.NORTH]
            case "-":
                return [Direction.EAST, Direction.WEST]


class MapGrid:
    def __init__(self, grid: list[list[Cell]]) -> None:
        self.grid = grid
        self.current: Optional[Cell] = None
        self.last: Optional[Cell] = None
        self.last_direction: Optional[Direction] = None

    @classmethod
    def from_input(cls, grid) -> "MapGrid":
        """Create a grid from the 2D string input array."""
        # Convert the string input to cell objects.
        for i, row in enumerate(grid):
            for j, pipe in enumerate(row):
                grid[i][j] = Cell((j, i), pipe)

        return cls(grid)

    @cached_property
    def size(self) -> tuple[int, int]:
        """Return the size of the grid."""
        return (len(self.grid[0]), len(self.grid))

    def build_loop(self, start_point: tuple[int, int]) -> None:
        """Build the loop and return the number of cells it contains."""
        self.current = self._at(start_point)
        self.last_direction = None

        result = 1
        while True:
            self._next()
            self.current.is_loop = True

            if self.current.indices == start_point:
                break

            result += 1

        return result

    def number_of_enclosed(self) -> int:
        """Return the number of cells enclosed by the loop."""
        count = 0
        for row in self.grid:
            for cell in row:
                if cell.is_loop:
                    continue

                # Count the number of pipe crosses in the provided direction.
                crosses = 0

                next_cell = cell
                while next_cell := self._cell_in_direction(next_cell, Direction.EAST):
                    if not next_cell.is_loop:
                        continue

                    crosses += next_cell.direction_value

                if crosses != 0:
                    cell.enclosed = True
                    count += 1

        return count

    def _at(self, indices: tuple[int, int]) -> Optional[Cell]:
        """Return the cell at the provided x, y indices.

        Return None if the cell does not exist.
        """
        if (indices[0] < 0 or indices[0] >= self.size[0]) or (
            indices[1] < 0 or indices[1] >= self.size[1]
        ):
            return None

        return self.grid[indices[1]][indices[0]]

    def _cell_in_direction(self, this_cell: Cell, direction: Direction) -> Optional[Cell]:
        """Get the cell in the provided direction.

        Return None if the direction goes off of the grid.
        """
        next_cell = (
            this_cell.indices[0] + direction.value[0],
            this_cell.indices[1] + direction.value[1],
        )
        return self._at(next_cell)

    def _next(self) -> None:
        """Advance to the next cell in the loop."""
        for direction in self.current.valid_directions():
            next_cell = self._cell_in_direction(self.current, direction)

            if not next_cell:
                continue

            if next_cell == self.last:
                continue

            if self.current.connected_to(next_cell, direction):
                self.last = self.current
                self.current = next_cell

                # Determine the direction the edge is traveling. This is used for counting crosses.
                for traveling_direction in [Direction.NORTH, Direction.SOUTH]:
                    if direction is traveling_direction:
                        self.current.direction_value = traveling_direction.value[1]

                        if self.last_direction != traveling_direction:
                            self.last.direction_value = self.current.direction_value

                        self.last_direction = traveling_direction

                return


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one = 0
    part_two = 0

    grid = []
    start_point = None
    for index, line in enumerate(file):
        line = line.strip()

        if "S" in line:
            start_point = (line.find("S"), index)

        grid.append(list(line))

    map_grid = MapGrid.from_input(grid)
    part_one = int(map_grid.build_loop(start_point) / 2)
    part_two = map_grid.number_of_enclosed()

    return part_one, part_two
