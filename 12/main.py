import fileinput
import re
from typing import Dict, Any

# ..........
# #.#.###... 0 2 4
# #.#..###.. 0 2 5
# #.#...###. 0 2 6
# #.#....### 0 2 7
# #..#.###.. 0 3 5
# #..#..###. 0 3 6

cache: dict[tuple[int, int], int] = {}


def inc_shifts(i: int, prev_end: int) -> int:
    if (i, prev_end) in cache:
        return cache[(i, prev_end)]

    if i == 0:
        shifts[0] = 0
    else:
        shifts[i] = shifts[i - 1] + lengths[i - 1] + 1

    counter = 0
    while shifts[i] + lengths[i] <= len(fmt):
        if (i, shifts[i]) in cache:
            counter += cache[(i, shifts[i])]
            break

        if '#' in fmt[prev_end:shifts[i]]:
            break
        # if '.' not in fmt[shifts[i]:shifts[i] + lengths[i]] :
        if '.' not in fmt[shifts[i]:shifts[i] + lengths[i]] and (i != len(shifts) - 1 or '#' not in fmt[shifts[i] + lengths[i]:]):
            if i == len(shifts) - 1:
                # print(shifts)
                res = ""
                for j in range(len(fmt)):
                    cnt = False
                    for k in range(len(shifts)):
                        if shifts[k] <= j < shifts[k] + lengths[k]:
                            cnt = True
                            break
                        if cnt: continue
                    res += "#" if cnt else "."
                # print(res)
                for j in range(len(fmt)):
                    if fmt[j] == "#":
                        if res[j] != "#":
                            print(fmt)
                            print(res)
                        assert res[j] == "#"
                    if fmt[j] == ".":
                        assert res[j] == "."
                counter += 1
            else:
                counter += inc_shifts(i + 1, shifts[i] + lengths[i])
        shifts[i] += 1

    cache[(i, prev_end)] = counter

    return counter


with fileinput.input(files=("input"), encoding="utf-8") as f:
    sum = 0
    for e, line in enumerate(f):
        cache = {}
        # if e != 1: continue
        fmt, lengths = line.rstrip("\n").split(" ")
        lengths = [int(i) for i in lengths.split(",")]
        new_lengths = []
        new_fmt = ""
        for i in range(5):
            new_lengths.extend(lengths)
            if i != 0: new_fmt += "?"
            new_fmt += fmt
        lengths = new_lengths
        fmt = new_fmt

        shifts = [0 for n in lengths]
        for i in range(len(shifts)):
            if i == 0:
                continue
            shifts[i] = shifts[i - 1] + lengths[i - 1] + 1

        # print(fmt)
        # print()
        count = inc_shifts(0, 0)
        print(count)
        sum += count

        # shifts[1] = shifts[0] + lengths[0] + 1
        # while shifts[1] + lengths[1] <= (length - lengths[2]):
        #     shifts[2] = shifts[1] + lengths[1] + 1
        #     while shifts[2] + lengths[2] <= length:
        #         print(shifts)
        #         shifts[2] += 1
        #     shifts[1] += 1
        # quit(0)

    print()
    print(sum)

    #                                 len   ?count
    # 1   1       1       1 * 1       7     3
    # 4   16384   4096    64 * 64     14    5
    # 1   1       1       1 * 1       15    8
    # 1   16      16      4 * 4       13    4
    # 4   2500    625     25 * 25     19    4
    # 10  506250  50625   225 * 225   12    9


    # ???.### 1,1,3 - 1 arrangement
    # .??..??...?##. 1,1,3 - 4 arrangements
    # ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    # ????.#...#... 4,1,1 - 1 arrangement
    # ????.######..#####. 1,6,5 - 4 arrangements
    # ?###???????? 3,2,1 - 10 arrangements
