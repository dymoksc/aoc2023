import fileinput
from math import gcd
from functools import reduce

instructions = ""
m: dict[str, tuple[str, str]] = {}
current_keys = []
with fileinput.input(files=('input'), encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 0:
            instructions = line.strip()
        if i > 1:
            key: str
            key, turns = line.split(" = ")
            left, right = turns.strip("()\n").split(', ')
            m[key] = (left, right)
            if key.endswith("A"):
                current_keys.append(key)

i = 0

z_count = 0
print(current_keys)
previous_z = [0 for _ in current_keys]
z_freq = [0 for _ in current_keys]
freq_stab = [0 for _ in current_keys]

while len([x for x in freq_stab if x < 1]) > 0:
    for j in range(len(current_keys)):
        current_keys[j] = m[current_keys[j]][0 if instructions[i % len(instructions)] == "L" else 1]
        if current_keys[j].endswith("Z"):
            if z_freq[j] == i - previous_z[j]:
                freq_stab[j] += 1
            else:
                freq_stab[j] -= 1
            z_freq[j] = i - previous_z[j]
            print(z_freq)
            previous_z[j] = i
    i += 1

lcm = reduce(lambda x, y: x * y // gcd(x, y), z_freq)
print(lcm)
