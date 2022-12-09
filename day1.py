from collections import deque

top_three = deque([0, 0, 0], maxlen=3)

maximum = 0
current = 0
with open("input/day1.txt", "r", encoding="utf-8") as file:
    for line in file:
        try:
            current += int(line)
        except ValueError:
            maximum = max(current, maximum)

            if current >= top_three[2]:
                top_three.append(current)
            elif current >= top_three[1]:
                top_three[0] = top_three[1]
                top_three[1] = current
            elif current < top_three[1] and current > top_three[0]:
                top_three[0] = current

            current = 0

print(sum(top_three))
print(maximum)
