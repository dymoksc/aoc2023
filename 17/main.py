import fileinput
from typing import Optional

Coords = tuple[int, int]
adjacency_list: dict[Coords, tuple[int, list[tuple[Coords, str]]]] = {}

rows: int = 0
cols: int = 0

field: list[list[int]] = []
with (fileinput.input(files=("input_sample"), encoding="utf-8") as f):
    for line in f:
        field.append([int(i) for i in line.rstrip('\n')])
rows = len(field)
cols = len(field[0])

INF = 99999999
dist: dict[Coords, int] = {}
prev: dict[Coords, Optional[tuple[Coords, str]]] = {}
q: list[Coords] = []
is_in_q: dict[Coords, bool] = {}

for i in range(rows - 1, -1, -1):
    for j in range(cols - 1, -1, -1):
        neighbors = []
        if i != 0: neighbors.append(((i - 1, j), '^'))
        if j != 0: neighbors.append(((i, j - 1), '<'))
        if i != len(field) - 1: neighbors.append(((i + 1, j), 'v'))
        if j != len(field[0]) - 1: neighbors.append(((i, j + 1), '>'))
        adjacency_list[(i, j)] = (field[i][j], neighbors)

        dist[(i, j)] = INF
        prev[(i, j)] = None
        q.append((i, j))
        is_in_q[(i, j)] = True
dist[(0, 0)] = 0

prev_dir = 'x'
same_dir_counter = 0
while len(q) != 0:
    u = q.pop()
    is_in_q[u] = False

    dir_history = ""
    vert = u
    while prev[vert] is not None and len(dir_history) < 3:
        dir_history = dir_history + prev[vert][1]
        vert = prev[vert][0]

    for v, dir in adjacency_list[u][1]:
        if not is_in_q[v]:
            continue
        if len(dir_history) == 3 and dir_history[0] == dir_history[1] == dir_history[2] == dir:
            continue

        alt = dist[u] + adjacency_list[u][0]
        if alt < dist[v]:
            dist[v] = alt
            prev[v] = (u, dir)

s_field = [[str(c) for c in line] for line in field]

# Retrieve path
s = []
u: tuple[int, int] = (len(s_field) - 1, len(s_field[0]) - 1)
dir = 'x'
if u in prev or u == (0, 0):
    while u is not None:
        s.insert(0, u)
        prev_rec = prev[u]
        if prev_rec is None:
            u = None
        else:
            u_new, dir = prev_rec
            s_field[u[0]][u[1]] = dir
            u = u_new

for line in s_field:
    print("".join(line))

print(dist[len(s_field) - 1, len(s_field[0]) - 1])

