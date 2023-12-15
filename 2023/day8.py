import math
from typing import TextIO, Tuple


def get_instructions_nodes(file: TextIO) -> dict:
    """Return instructions and nodes from input file."""
    instructions = file.readline().strip()

    nodes = {}
    for line in file:
        line = line.strip()

        if not line:
            continue

        node, elements = _parse_line(line)
        nodes[node] = elements

    return instructions, nodes


def solve(nodes, instructions, start: str) -> int:
    """Walk the nodes for the given instructions and return the number of steps."""
    node = start

    index = 0
    while not node.endswith("Z"):
        instruction = instructions[index % len(instructions)]

        node = nodes[node][instruction]

        index += 1

    return index


def _parse_line(line: str) -> Tuple[str, dict]:
    """Read the line into a dictionary with left and right elements."""
    node, elements = line.split("=")
    elements = elements.strip("( )").split(",")

    return node.strip(), {"L": elements[0].strip(), "R": elements[1].strip()}


def one(file: TextIO) -> int:
    """Run the solution for this day."""
    instructions, nodes = get_instructions_nodes(file)

    return solve(nodes, instructions, "AAA")


def two(file: TextIO) -> int:
    """Run the solution for this day."""
    instructions, nodes = get_instructions_nodes(file)

    values = []
    for name in filter(lambda name: name.endswith("A"), nodes.keys()):
        values.append(solve(nodes, instructions, name))

    return math.lcm(*values)
