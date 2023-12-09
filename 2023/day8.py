import math
from typing import TextIO, Tuple


def parse(line: str) -> Tuple[str, dict]:
    node, elements = line.split("=")
    elements = elements.strip("( )").split(",")

    return node.strip(), {"L": elements[0].strip(), "R": elements[1].strip()}


def solve(nodes, instructions, start: str) -> int:
    this_node_name = start
    index = 0
    while not this_node_name.endswith("Z"):
        instruction = instructions[index % len(instructions)]

        this_node_name = nodes[this_node_name][instruction]

        index += 1

    return index


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    instructions = file.readline().strip()

    nodes = {}
    a_node_names = []
    for line in file:
        line = line.strip()

        if not line:
            continue

        node, elements = parse(line)
        nodes[node] = elements

        if node.endswith("A"):
            a_node_names.append(node)

    values = []
    for node in a_node_names:
        values.append(solve(nodes, instructions, node))

    part_two = math.lcm(*values)

    return part_one, part_two
