import fileinput
import re

bag = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def process(line: str) -> int:
    for sample in line.rstrip("\n").split(": ")[1].split("; "):
        for n, color in re.findall("(\d+) ([^,]+)", sample):
            if bag[color] >= int(n):
                pass
            else:
                return 0
                return
    return int(line.rstrip("\n").split(": ")[0].split(" ")[1])


with fileinput.input(files=('input1'), encoding="utf-8") as f:
    print(sum(process(line) for line in f))
