import fileinput
import re
from functools import reduce

bag = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def process(line: str) -> int:
    req = {"red": 0, "green": 0, "blue": 0}
    for sample in line.rstrip("\n").split(": ")[1].split("; "):
        for n, color in re.findall("(\d+) ([^,]+)", sample):
            req[color] = max(int(n), req[color])
    return reduce(lambda x, y: x * y, list(req.values()))


with fileinput.input(files=('input1'), encoding="utf-8") as f:
    print(sum(process(line) for line in f))
