import fileinput
from typing import Dict, Any

instructions = ""
m: dict[str, tuple[str, str]] = {}
with fileinput.input(files=('input'), encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 0:
            instructions = line.strip()
        if i > 1:
            key, turns = line.split(" = ")
            left, right = turns.strip("()\n").split(', ')
            m[key] = (left, right)

current_key = "AAA"
i = 0
while current_key != "ZZZ":
    # print(current_key, m[current_key])
    # print(instructions[i % len(instructions)], [0 if instructions[i % len(instructions)] == "L" else 1])
    current_key = m[current_key][0 if instructions[i % len(instructions)] == "L" else 1]
    # print(current_key)
    i += 1

print(i)