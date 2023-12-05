import fileinput
from collections import namedtuple
from typing import Dict, Any, List

Mapping = namedtuple("Mapping", "dst_start src_start length")

with fileinput.input(files=('input'), encoding="utf-8") as f:
    key = None
    m: dict[str, list[Mapping]] = {}
    for n, line in enumerate(f):
        if n == 0:
            title, numbers = line.rstrip('\n').split(': ')
            assert title == "seeds"
            seeds = [int(i) for i in numbers.split()]
            print(seeds)
        elif line.endswith("map:\n"):
            key = line.split()[0]
            m[key] = []
        elif line != '\n':
            dst_start, src_start, length = [int(i) for i in line.rstrip('\n').split()]
            m[key].append(Mapping(dst_start, src_start, length))

    min_num = 999999999999
    for seed in seeds:
        print("Seed {}, ".format(seed), end="")
        num = seed

        for key, mappings in m.items():
            for mapping in mappings:
                if mapping.src_start <= num <= mapping.src_start + mapping.length:
                    num = mapping.dst_start + (num - mapping.src_start)
                    break
            print("{} {}, ".format(key.split('-')[-1], num), end="")
        print()

        if min_num > num:
            min_num = num

    print(min_num)