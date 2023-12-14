import fileinput

field: list[list[str]] = []
with fileinput.input(files=("input"), encoding="utf-8") as f:
    for line in f:
        field.append(list(line.rstrip("\n")))

for i in range(1, len(field)):
    for j in range(len(field[i])):
        if field[i][j] == 'O':
            for k in range(0, i):
                if field[i - k - 1][j] == '.':
                    field[i - k - 1][j], field[i - k][j] = field[i - k][j], field[i - k - 1][j]
                else:
                    break

load = 0
for i in range(len(field) - 1, -1, -1):
    multiplier = len(field) - i
    load += len([c for c in field[i] if c == 'O']) * multiplier

print(load)
