import fileinput
from typing import List, Any


def out_group(g: list[list[str]]):
    for g_line in g:
        print("".join(g_line))
    print()


def find_mirror(g: list[list[str]]) -> int:
    common_mirror_points: dict[int, int] = {}

    for i, _ in enumerate(g):
        line_mirror_points: dict[int, int] = {}
        for j, _ in enumerate(g[i]):
            k = 0
            if j != 0:
                smudges = 0
                while j + k < len(g[i]) and j - k - 1 >= 0:
                    if g[i][j + k] != g[i][j - k - 1]:
                        smudges += 1
                        if smudges > 1:
                            break
                    k += 1

                if 0 <= smudges <= 1:
                    line_mirror_points[j] = smudges

        if i == 0:
            if len(line_mirror_points) == 0:
                return 0
            common_mirror_points = line_mirror_points
        else:
            # common_mirror_points = [p for p in common_mirror_points if p in line_mirror_points]
            common_mirror_points = {pos: sm + line_mirror_points[pos] for pos, sm in common_mirror_points.items() if pos in line_mirror_points and sm + line_mirror_points[pos] < 2}
            if len(common_mirror_points) == 0:
                return 0

    # assert len(common_mirror_points) <= 1

    common_mirror_points = {pos: sm for pos, sm in common_mirror_points.items() if sm == 1}
    assert 0 <= len(common_mirror_points) <= 1

    return list(common_mirror_points.keys())[0] if len(common_mirror_points) == 1 else 0


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
            hor = find_mirror(group)
            if hor != 0:
                sum += hor
            else:
                ver = find_mirror(transpose(group))
                if ver != 0:
                    sum += ver * 100
            # out_group(group)
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