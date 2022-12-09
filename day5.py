from collections import deque


def get_move(line):
    words = line.split(" ")
    return int(words[1]), int(words[3]) - 1, int(words[5]) - 1


def build_stacks(rows):
    number_of_stacks = int(rows[-1].split(" ")[-1])

    stacks = []
    for index in range(number_of_stacks):
        stacks.append(deque())

    for row in rows[:-1]:
        for index, (_, crate, _) in enumerate(zip(row[0::4], row[1::4], row[2::4])):
            if crate != " ":
                stacks[index].appendleft(crate)

    return stacks


with open("input/day5.txt", "r", encoding="utf-8") as file:
    string = file.read()

rows, moves = string.split("\n\n")

stacks = build_stacks(rows.split("\n"))

for move in moves.split("\n"):
    number, source, destination = get_move(move)

    temp = deque()
    for i in range(number):
        temp.appendleft(stacks[source].pop())

    stacks[destination].extend(temp)

string = ""
for stack in stacks:
    string += stack.pop()

print(string)
