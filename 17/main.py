import fileinput

dir_history = 3

field: list[list[int]] = []
with (fileinput.input(files=("input_sample"), encoding="utf-8") as f):
    for line in f:
        field.append([int(i) for i in line.rstrip('\n')])

INF = 9999
invocations = 0
global_min = 9999


def explore(row: int, col: int, prev_dirs: str, visited: list[list[bool]], depth: int = 0, cur_dist: int = 0) -> tuple[int, list[tuple[int, int]]]:
    global invocations, global_min
    invocations += 1

    if cur_dist > global_min:
        return cur_dist, []

    if row == len(field) - 1 and col == len(field[0]) - 1:
        # for row in visited:
        #     print(row)
        # print()
        return cur_dist + field[col][row], [(row, col)]

    min_dist = INF
    min_trace = []
    visited[row][col] = True
    for dir in "><v^":
        if dir * dir_history == prev_dirs:
            continue
        new_row, new_col = row, col
        if dir == ">":
            new_col += 1
        if dir == "<":
            new_col -= 1
        if dir == "v":
            new_row += 1
        if dir == "^":
            new_row -= 1
        if new_row not in range(len(field)) or new_col not in range(len(field[0])) or visited[new_row][new_col]:
            continue

        dirs = dir + prev_dirs
        if len(dirs) > dir_history:
            dirs = dirs[:3]
        dist, trace = explore(new_row, new_col, dirs, visited, depth + 1, cur_dist + (field[col][row] if depth != 0 else 0))
        # dist += field[new_row][new_col]
        if dist < min_dist:
            min_dist = dist
            min_trace = trace
            if depth == 0:
                global_min = min_dist
                print(global_min)

    visited[row][col] = False
    # print(depth)

    return min_dist, min_trace + [(row, col)]


print(explore(0, 0, "", [[False for _ in line] for line in field]))
print(invocations)
