import copy
import fileinput

field: list[list[str]] = []
distances: list[list[int]] = []
max_steps = 64


def get_steps(coords: tuple[int, int], steps_count: int) -> list[tuple[int, int]]:
    steps = []

    potential_steps = [(coords[0] - 1, coords[1]),
                       (coords[0] + 1, coords[1]),
                       (coords[0], coords[1] - 1),
                       (coords[0], coords[1] + 1)]

    for potential_step in potential_steps:
        i, j = potential_step
        if field[i][j] == "." or field[i][j] == "O" and distances[i][j] > steps_count + 1:
            steps.append((i, j))

    return steps

generations: dict[int, list[tuple[int, int]]] = {i: [] for i in range(max_steps + 1)}


def make_steps(coords: tuple[int, int], steps_count: int = 0):
    if steps_count > max_steps:
        return

    distances[coords[0]][coords[1]] = steps_count
    field[coords[0]][coords[1]] = "O"
    generations[steps_count].append(coords)

    steps_from_here = get_steps(coords, steps_count)
    for i, step in enumerate(steps_from_here):
        # print("Calculating", steps_count, "step (", i, "/", len(steps_from_here), ")")
        make_steps(step, steps_count + 1)

    return


with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for i, line in enumerate(f):
        field.append([])
        for j, c in enumerate(line.rstrip('\n')):
            if c == "S":
                field[i].append(".")
                start = (i, j)
            else:
                field[i].append(c)

distances = [[9999 for _ in line] for line in field]
field_bak = copy.deepcopy(field)

make_steps(start)

steps_sum = 0
for i in range(max_steps, -1, -2):
    for step in generations[i]:
        if field_bak[step[0]][step[1]] != "O":
            steps_sum += 1
            field_bak[step[0]][step[1]] = "O"

print(steps_sum)

for i, _ in enumerate(field):
    for j, _ in enumerate(field[i]):
        # print(field_bak[i][j], end='')
        print("{: 5} ".format(distances[i][j]), end='')
    print()