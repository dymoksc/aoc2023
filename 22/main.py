import copy
import fileinput
import heapq
from collections import namedtuple
from typing import List, Any

Coord = namedtuple('Coord', 'x y z')
block_counter = 'A'


class Block:
    def __init__(self, c1: Coord, c2: Coord):
        global block_counter

        if c1.z < c2.z:
            self.low, self.high = c1, c2
        else:
            self.low, self.high = c2, c1
        self.counter = block_counter
        block_counter = chr(ord(block_counter) + 1)

    def __str__(self) -> str:
        return "{}: {} - {}".format(self.counter, self.low, self.high)

    def intersects_horizontally(self, other: 'Block') -> bool:
        # x1 <= y2 && y1 <= x2
        return min(self.low.x, self.high.x) <= max(other.low.x, other.high.x) and \
            min(other.low.x, other.high.x) <= max(self.low.x, self.high.x) and \
            min(self.low.y, self.high.y) <= max(other.low.y, other.high.y) and \
            min(other.low.y, other.high.y) <= max(self.low.y, self.high.y)

    def put_on(self, level: int):
        self.high = Coord(self.high.x, self.high.y, self.high.z - self.low.z + level + 1)
        self.low = Coord(self.low.x, self.low.y, level + 1)


# assert Block(Coord(0, 0, 0), Coord(1, 1, 0)).intersects_horizontally(Block(Coord(1, 1, 10),
#                                                                            Coord(2, 2, 11)))


blocks_in_air_by_low: list[Block] = []
min_x, min_y, min_z = 9999, 9999, 9999
max_x, max_y, max_z = -9999, -9999, -9999

i = 0
with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for line in f:
        c1_def, c2_def = [[int(i) for i in c.split(',')] for c in line.rstrip('\n').split('~')]
        heapq.heappush(blocks_in_air_by_low, (min(c1_def[2], c2_def[2]),
                                              i,
                                              Block(Coord(c1_def[0], c1_def[1], c1_def[2]),
                                                    Coord(c2_def[0], c2_def[1], c2_def[2]))))

        min_x, min_y, min_z = min(min_x, c1_def[0], c2_def[0]), min(min_y, c1_def[1], c2_def[1]), \
                                                                min(min_z, c1_def[2], c2_def[2])
        max_x, max_y, max_z = max(max_x, c1_def[0], c2_def[0]), max(max_y, c1_def[1], c2_def[1]), \
                                                                max(max_z, c1_def[2], c2_def[2])
        i += 1

field: list[list[list[str]]] = [[['.' for _ in range(max_z + 1)] for _ in range(max_y + 1)]
                                for _ in range(max_x + 1)]

lying_blocks_by_high: list[Block] = []
dependencies: dict[Block, list[Block]] = {}
reverse_deps: dict[Block, list[Block]] = {}

collision_counter = 0
while len(blocks_in_air_by_low) != 0:
    b: Block
    _, _, b = heapq.heappop(blocks_in_air_by_low)

    lie_on_level = 0
    depend_on_blocks = []
    insert_on_index = 0

    # for i, lb in enumerate(lying_blocks_by_high):
    blocks_to_return: list[Block] = []
    while len(lying_blocks_by_high) != 0:
        _, _, lb = heapq.heappop(lying_blocks_by_high)
        blocks_to_return.append(lb)

        if (lie_on_level == 0 or lie_on_level == lb.high.z) and lb.intersects_horizontally(b):
            # if lie_on_level == 0:
            #     insert_on_index = i
            # else:
            #     if depend_on_blocks[-1].high.z != lb.high.z:
            #         pass
            #     assert depend_on_blocks[-1].high.z == lb.high.z
            lie_on_level = lb.high.z
            depend_on_blocks.append(lb)
            reverse_deps[lb].append(b)
        elif lie_on_level > lb.high.z:
            break

    for b2r in blocks_to_return:
        heapq.heappush(lying_blocks_by_high, (-b2r.high.z, collision_counter, b2r))
        collision_counter += 1
    b.put_on(lie_on_level)
    # lying_blocks_by_high.insert(insert_on_index, b)
    heapq.heappush(lying_blocks_by_high, (-b.high.z, collision_counter, b))
    collision_counter += 1
    dependencies[b] = depend_on_blocks
    reverse_deps[b] = []

    for i in range(min(b.low.x, b.high.x), max(b.low.x, b.high.x) + 1):
        for j in range(min(b.low.y, b.high.y), max(b.low.y, b.high.y) + 1):
            for k in range(min(b.low.z, b.high.z), max(b.low.z, b.high.z) + 1):
                field[i][j][k] = b.counter


def get_fallen(b: Block) -> list[Block]:
    fallen = [b]
    for dep in reverse_deps[b]:
        fallen.extend(get_fallen(dep))
    return fallen


def disintegrate(bs: list[Block]) -> int:
    cnt = 0
    for b in bs:
        for dependant in reverse_deps[b]:
            if len([dep for dep in dependencies[dependant] if dep not in bs]) == 0 and dependant not in bs:
                bs.append(dependant)
                cnt += 1
    return cnt

# for _, _, b in lying_blocks_by_high:
#     print(b.counter, disintegrate([b]))

print(sum([disintegrate([b]) for _, _, b in lying_blocks_by_high]))

# for k in range(max_z, -1, -1):
#     for i in range(max_x + 1):
#         char = '.'
#         for j in range(max_y + 1):
#             if field[i][j][k] != '.':
#                 if char == '.':
#                     char = field[i][j][k]
#                 elif char != field[i][j][k]:
#                     char = '?'
#         print(char, end="")
#     print()
#
# print()
#
# for k in range(max_z, -1, -1):
#     for j in range(max_y + 1):
#         char = '.'
#         for i in range(max_x + 1):
#             if field[i][j][k] != '.':
#                 if char == '.':
#                     char = field[i][j][k]
#                 elif char != field[i][j][k]:
#                     char = '?'
#         print(char, end="")
#     print()
#
# print()

# print([str(b) for _, b in blocks_in_air_by_low])
# print([str(b) for _, b in lying_blocks_by_high])

