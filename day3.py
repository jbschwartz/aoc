from collections import Counter


def priority(char):
    if ord("a") <= ord(char) <= ord("z"):
        return ord(char) - ord("a") + 1

    if ord("A") <= ord(char) <= ord("Z"):
        return ord(char) - ord("A") + 27


score = 0
with open("input/day3.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        compartment_size = int(len(line) / 2)
        first, second = line[:compartment_size], line[compartment_size:]

        for char in second:
            if char in first:
                score += priority(char)
                break

print(score)

score = 0
with open("input/day3.txt", "r", encoding="utf-8") as file:
    for lines in zip(file, file, file):
        lines = list(map(lambda l: set(l.strip()), lines))

        common = list(set.intersection(*lines))[0]

        score += priority(common)

print(score)
