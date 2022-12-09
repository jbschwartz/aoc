import dataclasses


@dataclasses.dataclass
class Tree:
    height: int
    visible: bool
    edge: bool
    score: int


class Grid:
    def __init__(self):
        self.rows = []

    @property
    def columns(self):
        columns = []
        for index in range(len(self.rows[0])):
            columns.append([row[index] for row in self.rows])

        return columns

    def add_row(self, row_string):
        row = []
        for height in row_string:
            row.append(Tree(int(height), False, True, 0))

        if len(self.rows) > 1:
            for tree in self.rows[-1][1:-1]:
                tree.edge = False

        self.rows.append(row)

    def show(self, mark_edge=False):
        for row in self.rows:
            string = ""
            for show_visible in [False, True]:
                string += " "

                for tree in row:
                    if show_visible:
                        if tree.visible or tree.edge:
                            string += "v"
                        else:
                            string += "."
                    else:
                        string += str(tree.height)

            print(string)
        print()

    def compute_score(self, x, y):
        left = self.rows[y][0:x][::-1]
        right = self.rows[y][x + 1 :]
        up = self.columns[x][0:y][::-1]
        down = self.columns[x][y + 1 :]

        this_tree = self.rows[y][x]

        total_score = 1
        for direction in [up, left, down, right]:
            score = 0
            for tree in direction:
                score += 1
                if tree.height >= this_tree.height:
                    break

            total_score *= score

        this_tree.score = total_score

    def compute_scores(self):
        for y, row in enumerate(self.rows):
            for x in range(len(row)):
                self.compute_score(x, y)

    def compute_visibility(self):
        for direction in [self.rows, self.columns]:
            for line in direction:
                for order in [line, line[::-1]]:
                    tallest = 0
                    for tree in order:
                        if tree.height > tallest:
                            tallest = tree.height
                            tree.visible = True

    def total_visible(self):
        total = 0
        for row in self.rows:
            for tree in row:
                if tree.visible or tree.edge:
                    total += 1

        return total

    def highest_score(self):
        highest = 0
        for row in self.rows:
            for tree in row:
                if tree.score > highest:
                    highest = tree.score

        return highest


grid = Grid()

with open("input/day8.txt", "r", encoding="utf-8") as file:
    for line in file:
        grid.add_row(line.strip())

grid.compute_visibility()

grid.show(True)
print(grid.total_visible())

grid.compute_scores()
print(grid.highest_score())
