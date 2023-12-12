import fileinput

# ..........
# #.#.###... 0 2 4
# #.#..###.. 0 2 5
# #.#...###. 0 2 6
# #.#....### 0 2 7
# #..#.###.. 0 3 5
# #..#..###. 0 3 6


def inc_shifts(i: int, prev_end: int) -> int:
    if i == 0:
        shifts[0] = 0
    else:
        shifts[i] = shifts[i - 1] + lengths[i - 1] + 1

    counter = 0
    while shifts[i] + lengths[i] <= len(fmt):
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

    return counter


with fileinput.input(files=("input"), encoding="utf-8") as f:
    sum = 0
    for e, line in enumerate(f):
        # if e != 1: continue
        fmt, lengths = line.rstrip("\n").split(" ")
        lengths = [int(i) for i in lengths.split(",")]

        shifts = [0 for n in lengths]
        for i in range(len(shifts)):
            if i == 0:
                continue
            shifts[i] = shifts[i - 1] + lengths[i - 1] + 1

        # print(fmt)
        # print()
        sum += inc_shifts(0, 0)

        # shifts[1] = shifts[0] + lengths[0] + 1
        # while shifts[1] + lengths[1] <= (length - lengths[2]):
        #     shifts[2] = shifts[1] + lengths[1] + 1
        #     while shifts[2] + lengths[2] <= length:
        #         print(shifts)
        #         shifts[2] += 1
        #     shifts[1] += 1

    print(sum)