import fileinput
import re
from collections import namedtuple

Condition = namedtuple("Condition", "attr sign num result")

auto: dict[str, list[Condition]] = {}
flows = []
parts = []


def consider(p) -> bool:
    flow = "in"
    while True:
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
                    return True
                elif res == 'R':
                    return False
                else:
                    finish_current_automaton = True
                    flow = res
                    break


edges = []
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
                edges.append((n.group(2), int(n.group(3))))
                auto[m.group(1)].append(Condition(n.group(1), n.group(2), int(n.group(3)), n.group(4)))

    for line in f:
        parts.append({k: int(v) for k, v in [assign.split('=') for assign in line.strip('{}\n').split(',')]})

edges.sort(key=lambda edge: edge[1])
print(edges)
# attr_sums = 0
# for part in parts:
#     # print(part, consider(part))
#     if consider(part):
#         attr_sums += sum(list(part.values()))
# print(attr_sums)