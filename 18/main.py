import fileinput


def determinant(m0: tuple[int, int], m1: tuple[int, int]) -> int:
    return m0[0] * m1[1] - m1[0] * m0[1]


def area(points: list[tuple[int, int]]) -> float:
    # moved_col = [False for _ in points]
    # moved_row = [False for _ in points]

    # print(points)

    det_sum = 0
    for i in range(len(points)):
        j = (i + 1) % len(points)

        if points[i][0] == points[j][0]:
            # Horizontal line
            pts1 = points[i]
            pts2 = points[j]
            det = determinant(pts1, pts2)
            pts1 = (points[i][0] - 1, points[i][1])
            pts2 = (points[j][0] - 1, points[j][1])
            det_mod = determinant(pts1, pts2)
            if det_mod < det:
                points[i] = pts1
                points[j] = pts2
                det_sum += det_mod
            else:
                det_sum += det
        elif points[i][1] == points[j][1]:
            # Vertical line
            pts1 = points[i]
            pts2 = points[j]
            det = determinant(pts1, pts2)
            pts1 = (points[i][0], points[i][1] + 1)
            pts2 = (points[j][0], points[j][1] + 1)
            det_mod = determinant(pts1, pts2)
            if det_mod < det:
                points[i] = pts1
                points[j] = pts2
                det_sum += det_mod
            else:
                det_sum += det
        else:
            assert False

    # print(points)

    # return det_sum / 2

    return sum([determinant(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]) // 2


instructions = []
max_i = 0
min_i = 9999
max_j = 0
min_j = 9999

print("Reading instructions")
pts: list[tuple[int, int]] = []
with (fileinput.input(files=("input"), encoding="utf-8") as f):
    i = 0
    j = 0
    for line in f:
        _, _, color = line.rstrip('\n').split()
        direction = 'RDLU'[int(color[7])]
        count = int("0x" + color[2:7], 0)
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
        pts.append((i, j))

max_i += 1
max_j += 1

# rows = max_i - min_i
# cols = max_j - min_j

# field = [['.' for _ in range(cols)] for _ in range(rows)]
# i = 0
# j = 0

# print("Filling field")
# for direction, count, _ in instructions:
#     # print(direction, count, i, j)
#     if direction in 'UD':
#         if direction == 'U':
#             rng = (i, i - count - 1, -1)
#         if direction == 'D':
#             rng = (i, i + count + 1, 1)
#         for m in range(rng[0], rng[1], rng[2]):
#             field[m - min_i][j - min_j] = 'T' if direction == 'D' else 'L'
#         i = m
#     if direction in 'LR':
#         if direction == 'L':
#             rng = (j, j - count - 1, -1)
#         if direction == 'R':
#             rng = (j, j + count + 1, 1)
#         for n in range(rng[0], rng[1], rng[2]):
#             field[i - min_i][n - min_j] = '#' if field[i - min_i][n - min_j] == '.' else field[i - min_i][n - min_j]
#         j = n

# print("Tracing")
# for i in range(0, rows):
#     border_pieces_met = 0
#     prev = '.'
#     start = ''
#     for j in range(cols):
#         if prev != '.' and field[i][j] == '.' and prev == start:
#             border_pieces_met += 1
#         if prev == '.' and field[i][j] != '.':
#             start = field[i][j]
#         prev = field[i][j]
#         field[i][j] = 'o' if border_pieces_met % 2 == 1 and field[i][j] == '.' else field[i][j]

# for row in field:
#     print(''.join([c for c in row]))


# print(sum([sum([1 for c in row if c != '.']) for row in field]))

# print(pts)
max_area = area(pts)
print(max_area)

# moved_y = [False for _ in pts]
# moved_x = [False for _ in pts]
# for i in range(int(len(pts))):
#     p1 = i
#
#     pts[p1] = (pts[p1][0] - 1, pts[p1][1])
#     a = abs(area(pts))
#     if a < max_area:
#         pts[p1] = (pts[p1][0] + 1, pts[p1][1])
#     else:
#         max_area = a
#
#     pts[p1] = (pts[p1][0], pts[p1][1] + 1)
#     a = abs(area(pts))
#     if a < max_area:
#         pts[p1] = (pts[p1][0], pts[p1][1] + 1)
#     else:
#         max_area = a

# print(pts)
# print(max_area)
