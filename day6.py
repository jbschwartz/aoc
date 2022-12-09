with open("input/day6.txt", "r", encoding="utf-8") as file:
    line = file.read()

for index, window in enumerate(zip(line[0::1], line[1::1], line[2::1], line[3::1])):
    if len(set(window)) == len(window):
        break

print(index + 4)

window_size = 14
for index in range(len(line) - window_size + 1):
    window = line[index : index + window_size]
    if len(set(window)) == len(window):
        break

print(index + window_size)
