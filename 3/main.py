import fileinput
import re
from functools import reduce

with fileinput.input(files=('input'), encoding="utf-8") as f:
    lines = [l.rstrip() for l in f]

sum = 0
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == '*':
            added: dict[tuple[int, int], int] = {}
            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    if i + y_offset == -1 or i + y_offset == len(lines) \
                            or j + x_offset == -1 or j + x_offset == len(lines[0]):
                        continue
                    if '0' <= lines[i + y_offset][j + x_offset] <= '9':
                        x_number_start = j + x_offset
                        while x_number_start != 0 and \
                                '0' <= lines[i + y_offset][x_number_start - 1] <= '9':
                            x_number_start -= 1
                        if (i + y_offset, x_number_start) not in added:
                            res = re.search(r'\d+', lines[i + y_offset][x_number_start:]).group()
                            added[(i + y_offset, x_number_start)] = res
            if len(added) == 2:
                sum += reduce(lambda x, y: x * y, list(int(i) for i in added.values()))

print(sum)

# print(sum(list(int(i) for i in added.values())))

# for i in range(len(lines)):
#     skip = 0
#     for j in range(len(lines[0])):
#         if skip != 0:
#             skip -= 1
#             continue
#         if (i, j) in added:
#             print('X' * len(added[(i, j)]), end='')
#             skip = len(added[(i, j)]) - 1
#             continue
#         print(lines[i][j], end='')
#     print()
