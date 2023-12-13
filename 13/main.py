import fileinput
from typing import List, Any


def out_group(g: list[list[str]]):
    for g_line in g:
        print("".join(g_line))
    print()


def find_mirror(g: list[list[str]]) -> int:
    common_mirror_points: list[int] = []

    for i, _ in enumerate(g):
        line_mirror_points: list[int] = []
        for j, _ in enumerate(g[i]):
            k = 0
            if j != 0:
                mirror_point = True
                while j + k < len(g[i]) and j - k - 1 >= 0:
                    if g[i][j + k] != g[i][j - k - 1]:
                        mirror_point = False
                        break
                    k += 1
                if mirror_point:
                    line_mirror_points.append(j)

        if i == 0:
            if len(line_mirror_points) == 0:
                return 0
            common_mirror_points = line_mirror_points
        else:
            common_mirror_points = [p for p in common_mirror_points if p in line_mirror_points]
            if len(common_mirror_points) == 0:
                return 0

    assert len(common_mirror_points) <= 1

    return common_mirror_points[0] if len(common_mirror_points) == 1 else 0


def transpose(original: list[list[str]]) -> list[list[str]]:
    transposed = []
    for i in range(len(original[0])):
        transposed.append([])
        for j in range(len(original)):
            transposed[i].append(original[j][i])
    return transposed

with fileinput.input(files=("input"), encoding="utf-8") as f:
    sum = 0
    group = []
    for line in f:
        if line == "\n":
            # out_group(group)
            hor = find_mirror(group)
            if hor != 0:
                sum += hor
            else:
                ver = find_mirror(transpose(group))
                if ver != 0:
                    sum += ver * 100
            # print(find_mirror(group))
            # out_group(transpose(group))
            # print(find_mirror(transpose(group)))
            group = []
            continue
        group.append(list(line.rstrip("\n")))
    # out_group(group)
    # print(find_mirror(group))
    # out_group(transpose(group))
    # print(find_mirror(transpose(group)))

    hor = find_mirror(group)
    if hor != 0:
        sum += hor
    else:
        ver = find_mirror(transpose(group))
        if ver != 0:
            sum += ver * 100

    print(sum)