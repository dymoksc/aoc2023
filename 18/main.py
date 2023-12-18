import fileinput

instructions = []
max_i = 0
min_i = 9999
max_j = 0
min_j = 9999

print("Reading instructions")
with (fileinput.input(files=("input_sample"), encoding="utf-8") as f):
    i = 0
    j = 0
    for line in f:
        direction, count, color = line.rstrip('\n').split()
        instructions.append((direction, int(count), color))
        if direction == 'U':
            i -= int(count)
        if direction == 'D':
            i += int(count)
        if direction == 'R':
            j += int(count)
        if direction == 'L':
            j -= int(count)
        max_i = max(max_i, i)
        max_j = max(max_j, j)
        min_i = min(min_i, i)
        min_j = min(min_j, j)

max_i += 1
max_j += 1

rows = max_i - min_i
cols = max_j - min_j

field = [['.' for _ in range(cols)] for _ in range(rows)]
i = 0
j = 0

print("Filling field")
for direction, count, _ in instructions:
    # print(direction, count, i, j)
    if direction in 'UD':
        if direction == 'U':
            rng = (i, i - count - 1, -1)
        if direction == 'D':
            rng = (i, i + count + 1, 1)
        for m in range(rng[0], rng[1], rng[2]):
            field[m - min_i][j - min_j] = 'T' if direction == 'D' else 'L'
        i = m
    if direction in 'LR':
        if direction == 'L':
            rng = (j, j - count - 1, -1)
        if direction == 'R':
            rng = (j, j + count + 1, 1)
        for n in range(rng[0], rng[1], rng[2]):
            field[i - min_i][n - min_j] = '#' if field[i - min_i][n - min_j] == '.' else field[i - min_i][n - min_j]
        j = n

print("Tracing")
for i in range(0, rows):
    border_pieces_met = 0
    prev = '.'
    start = ''
    for j in range(cols):
        if prev != '.' and field[i][j] == '.' and prev == start:
            border_pieces_met += 1
        if prev == '.' and field[i][j] != '.':
            start = field[i][j]
        prev = field[i][j]
        field[i][j] = 'o' if border_pieces_met % 2 == 1 and field[i][j] == '.' else field[i][j]

# for row in field:
#     print(''.join([c for c in row]))

print(sum([sum([1 for c in row if c != '.']) for row in field]))
