import fileinput
import sys

sys.setrecursionlimit(20000)

field: list[list[str]] = []
with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for line in f:
        field.append(list(line.rstrip()))

start = (0, field[0].index('.'))
finish = (len(field) - 1, field[-1].index('.'))


def explore(i: int, j: int, st: int = 0) -> (int, bool):
    if i == finish[0] and j == finish[1]:
        return 1, True

    s = 0
    orig_c = field[i][j]
    field[i][j] = 'O'
    if orig_c in '.^' and i > 0 and field[i - 1][j] not in '#O':
        steps, reached_finish = explore(i - 1, j, st + 1)
        if reached_finish:
            s = max(s, steps)
    if orig_c in '.v' and i < len(field) - 1 and field[i + 1][j] not in '#O':
        steps, reached_finish = explore(i + 1, j, st + 1)
        if reached_finish:
            s = max(s, steps)
    if orig_c in '.<' and j > 0 and field[i][j - 1] not in '#O':
        steps, reached_finish = explore(i, j - 1, st + 1)
        if reached_finish:
            s = max(s, steps)
    if orig_c in '.>' and j < len(field[i]) - 1 and field[i][j + 1] not in '#O':
        steps, reached_finish = explore(i, j + 1, st + 1)
        if reached_finish:
            s = max(s, steps)
    field[i][j] = orig_c

    if s == 0:
        return 0, False

    return s + 1, True


steps, reached = explore(start[0], start[1])
print(steps - 1)
# for line in field:
#     for c in line:
#         print(c, end="")
#     print()
