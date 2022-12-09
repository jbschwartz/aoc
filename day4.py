score = 0
with open("input/day4.txt", "r", encoding="utf-8") as file:
    for line in file:
        first, second = list(map(lambda l: l.split("-"), line.strip().split(",")))

        first = list(map(int, first))
        second = list(map(int, second))

        if first[0] <= second[0] and first[1] >= second[1]:
            print("A", first, second)
            score += 1
        elif second[0] <= first[0] and second[1] >= first[1]:
            print("B", first, second)
            score += 1

print(score)

score = 0
with open("input/day4.txt", "r", encoding="utf-8") as file:
    for line in file:
        first, second = list(map(lambda l: l.split("-"), line.strip().split(",")))

        first = list(map(int, first))
        second = list(map(int, second))

        if first[1] < second[0] or first[0] > second[1]:
            continue

        score += 1

print(score)
