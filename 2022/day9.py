class Node:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.tail = None

        self.positions = {(0, 0)}

    def has(self, x, y, index=0):
        if self.x == x and self.y == y:
            return index

        if self.tail is None:
            return None

        return self.tail.has(x, y, index + 1)

    def move(self, direction, amount=1):
        step_function = getattr(self, f"_{direction.lower()}")

        for _ in range(amount):
            step_function()

            if self.tail is not None:
                self.tail.update(self.x, self.y)

            # show(self, 10, 10)

    def update(self, head_x, head_y):
        dx = head_x - self.x
        dy = head_y - self.y

        if abs(dx) == 2 and abs(dy) == 2:
            self.x += int(dx / 2)
            self.y += int(dy / 2)
        elif abs(dx) == 2:
            self.x += int(dx / 2)
            self.y = head_y
        elif abs(dy) == 2:
            self.y += int(dy / 2)
            self.x = head_x

        self.positions.add((self.x, self.y))

        if self.tail is not None:
            self.tail.update(self.x, self.y)

    def _r(self):
        self.x += 1

    def _u(self):
        self.y += 1

    def _l(self):
        self.x -= 1

    def _d(self):
        self.y -= 1


def show(head, width, height):
    for y in range(height)[::-1]:
        row = ""
        for x in range(width):
            index = head.has(x, y)
            if index is not None:
                if index == 0:
                    row += "H"
                else:
                    row += str(index)
            elif x == 0 and y == 0:
                row += "s"
            else:
                row += "."

        print(row)
    print("")


length = 10

nodes = [Node()]
for index in range(1, length):
    new_node = Node()
    nodes[index - 1].tail = new_node
    nodes.append(new_node)

head = nodes[0]
tail = nodes[-1]

with open("input/day9.txt", "r", encoding="utf-8") as file:
    for line in file:
        direction, amount = line.strip().split(" ")
        head.move(direction, int(amount))

print(len(tail.positions))
