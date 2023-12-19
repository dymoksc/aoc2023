import copy
import fileinput
import re
from collections import namedtuple
from functools import reduce

Condition = namedtuple("Condition", "attr sign num result")

auto: dict[str, list[Condition]] = {}
flows = []
parts = []


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_ranges: list[tuple[int, int]] = []
    while len(ranges) != 0:
        rng = ranges.pop()
        i = 0
        while i < len(ranges):
            # x1 <= y2 && y1 <= x2
            if rng[0] <= ranges[i][1] and ranges[i][0] <= rng[1]:
                rng = (min(rng[0], ranges[i][0]), max(rng[1], ranges[i][1]))
                ranges.pop(i)
            else:
                i += 1
        new_ranges.append(rng)
    return new_ranges


assert sorted(merge_ranges([(1, 4), (3, 5), (8, 9)])) == sorted([(1, 5), (8, 9)])


empty_part = {"x": (0, 0), "m": (0, 0), "a": (0, 0), "s": (0, 0)}


accepted = []

def consider(p: dict[str, tuple[int, int]], flow: str = "in", c_ind: int = 0, trace: list[str] = []):
    cond = auto[flow][c_ind]
    mod_p = copy.deepcopy(p)

    if cond.sign == '>':
        if p[cond.attr][1] > cond.num + 2:  # True branch
            if cond.result == "R":
                pass
            elif cond.result == "A":
                mod_p[cond.attr] = (max(p[cond.attr][0], cond.num + 1), p[cond.attr][1])
                accepted.append(mod_p)
                print(trace + [flow], mod_p)
            else:
                mod_p[cond.attr] = (max(p[cond.attr][0], cond.num + 1), p[cond.attr][1])
                consider(mod_p, cond.result, 0, trace + [flow])
        if p[cond.attr][0] <= cond.num:  # False branch
            mod_p_alt = copy.deepcopy(p)
            mod_p_alt[cond.attr] = (p[cond.attr][0], cond.num + 1)
            consider(mod_p_alt, flow, c_ind + 1, trace + [flow])
    elif cond.sign == '<':
        if p[cond.attr][0] < cond.num:  # True branch
            if cond.result == "R":
                pass
            elif cond.result == "A":
                mod_p[cond.attr] = (p[cond.attr][0], cond.num)
                accepted.append(mod_p)
                print(trace + [flow], mod_p)
            else:
                mod_p[cond.attr] = (p[cond.attr][0], cond.num)
                consider(mod_p, cond.result, 0, trace + [flow])
        if p[cond.attr][1] > cond.num - 1:  # False branch
            mod_p_alt = copy.deepcopy(p)
            mod_p_alt[cond.attr] = (cond.num, p[cond.attr][1])
            consider(mod_p_alt, flow, c_ind + 1, trace + [flow])
    else:
        consider(p, flow, c_ind + 1, trace + [flow])


def consider1(p) -> (bool, list[str]):
    global auto

    trace = []
    flow = "in"
    while True:
        trace.append(flow)
        automaton_conds = auto[flow]
        finish_current_automaton = False
        while not finish_current_automaton:
            for cond in automaton_conds:
                res = None
                if cond.sign == '>' and p[cond.attr] > cond.num or cond.sign == '<' and p[cond.attr] < cond.num:
                    res = cond.result
                if res is None:
                    continue
                elif res == 'A':
                    return True, trace
                elif res == 'R':
                    return False, trace
                else:
                    finish_current_automaton = True
                    flow = res
                    break


with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for line in f:
        m = re.match('(\w+)\{(.*)}\n', line)
        if m is None:
            break
        flows.append(m.group(1))
        auto[m.group(1)] = []
        for cond_des in m.group(2).split(","):
            n = re.match('([xmas])([<>])(\d+):(\w+)', cond_des)
            if n is None:
                auto[m.group(1)].append(Condition('x', '>', 0, cond_des))
            else:
                auto[m.group(1)].append(Condition(n.group(1), n.group(2), int(n.group(3)), n.group(4)))

    for line in f:
        parts.append({k: int(v) for k, v in [assign.split('=') for assign in line.strip('{}\n').split(',')]})

# # ['in', 'px', 'qkq'] {'x': (1, 1416), 'm': (1, 4001), 'a': (1, 2006), 's': (1, 1351)}
# for acc in accepted:
#     for x in [1, 1415]:
#         for m in [1, 4000]:
#             for a in [1, 2005]:
#                 for s in [1, 1350]:
#                     res, trace = consider1({"x": x, "m": m, "a": a, "s": s})
#                     assert (res, trace) == (True, ['in', 'px', 'qkq']), trace
#
# # ['in', 'in', 'qqz', 'qqz', 'hdj', 'hdj', 'pv', 'pv'] {'x': (1, 4001), 'm': (1, 839), 'a': (1, 1717), 's': (1, 2771)}
# for x in [1, 4000]:
#     for m in [1, 838]:
#         for a in [1, 1716]:
#             for s in [1, 2770]:
#                 res, trace = consider1({"x": x, "m": m, "a": a, "s": s})
#                 print(trace)
#                 assert res
#                 # assert (res, trace) == (True, ['in', 'qqz', 'hdj', 'pv']), trace


def get_volume(p: dict[str, tuple[int, int]]) -> int:
    vol = 1
    for rng in p.values():
        vol *= rng[1] - rng[0]
    return vol


assert get_volume({"x": (0, 2), "y": (0, 2)}) == 4
assert get_volume({"x": (0, 2), "y": (0, 2), "z": (0, 3)}) == 12


def get_intersection_volume(p1: dict[str, tuple[int, int]], p2: dict[str, tuple[int, int]]) -> int:
    # x1 <= y2 && y1 <= x2

    vol = 1
    for c in p1.keys():
        intersection = min(p1[c][1], p2[c][1]) - max(p1[c][0], p2[c][0])
        if intersection <= 0:
            return 0
        vol *= intersection

    return vol


assert get_intersection_volume({"x": (0, 2), "y": (0, 2)}, {"x": (1, 3), "y": (1, 3)}) == 1
assert get_volume({"x": (0, 2), "y": (0, 2)}) - \
       get_intersection_volume({"x": (0, 2), "y": (0, 2)}, {"x": (1, 3), "y": (1, 3)}) + \
       get_volume({"x": (1, 3), "y": (1, 3)}) == 7


consider({"x": (1, 4001), "m": (1, 4001), "a": (1, 4001), "s": (1, 4001)})

for acc in accepted:
    for x in [acc["x"][0], acc["x"][1] - 1]:
        for m in [acc["m"][0], acc["m"][1] - 1]:
            for a in [acc["a"][0], acc["a"][1] - 1]:
                for s in [acc["s"][0], acc["s"][1] - 1]:
                    res, _ = consider1({"x": x, "m": m, "a": a, "s": s})
                    if not res:
                        # ['in', 'mb', 'hvq', 'hsn', 'drn', 'drn', 'drn', 'jff', 'jff', 'jn', 'jn', 'jn'] {'x': (1, 4001), 'm': (611, 1446), 'a': (3252, 3412), 's': (1, 804)}
                        pass
                    assert res
                    # assert (res, trace) == (True, ['in', 'px', 'qkq']), trace

# 167409079868000
# 183726960685100

vol_sum = 0
for i in range(len(accepted)):
    vol_sum += get_volume(accepted[i])
    for j in range(i + 1, len(accepted)):
        vol_sum -= get_intersection_volume(accepted[i], accepted[j])
print(vol_sum)
