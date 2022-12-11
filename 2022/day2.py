score = 0
with open("input/day2.txt", "r", encoding="utf-8") as file:
    for line in file:
        opponent, _, you = map(ord, line.strip())
        opponent -= ord("A") - 1
        you -= ord("X") - 1

        score += you

        if you == opponent:
            score += 3
            continue

        if you == 1:
            if opponent == 2:
                continue
            if opponent == 3:
                score += 6

        elif you == 2:
            if opponent == 1:
                score += 6
            if opponent == 3:
                continue

        elif you == 3:
            if opponent == 1:
                continue
            if opponent == 2:
                score += 6

print(score)

score = 0
with open("input/day2.txt", "r", encoding="utf-8") as file:
    for line in file:
        opponent, _, outcome = map(ord, line.strip())
        opponent -= ord("A") - 1
        outcome = 3 * (outcome - ord("X"))

        score += outcome

        if outcome == 3:
            score += opponent
            continue

        if outcome == 0:
            if opponent == 1:
                score += 3
            if opponent == 2:
                score += 1
            if opponent == 3:
                score += 2
        elif outcome == 6:
            if opponent == 1:
                score += 2
            if opponent == 2:
                score += 3
            if opponent == 3:
                score += 1

print(score)
