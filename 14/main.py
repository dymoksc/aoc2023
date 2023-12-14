import fileinput

cycles = 1000000000

field: list[list[str]] = []
with fileinput.input(files=("input"), encoding="utf-8") as f:
    for line in f:
        field.append(list(line.rstrip("\n")))

cache = {}
prev_hash = None
hash1 = None
cycle = -1
established_cycle = False
while cycle < (cycles - 1):
    cycle += 1
    if hash1 in cache and cache[hash1]['next'] is not None:
        cache_cycle_len = 1
        current_cache_rec = cache[hash1]['next']
        while current_cache_rec != hash1:
            cache_cycle_len += 1
            current_cache_rec = cache[current_cache_rec]["next"]

        cycle += (cycles - cycle - 1) // cache_cycle_len * cache_cycle_len

        prev_hash = hash1
        hash1 = cache[hash1]['next']
        # print("fast", cycle)

        continue

    prev_hash = hash1
    # print("manual", cycle)

    for direction in ['north', 'west', 'south', 'east']:
        if direction == 'north':
            for i in range(1, len(field)):
                for j in range(len(field[i])):
                    if field[i][j] == 'O':
                        for k in range(0, i):
                            if field[i - k - 1][j] == '.':
                                field[i - k - 1][j], field[i - k][j] = field[i - k][j], field[i - k - 1][j]
                            else:
                                break
        if direction == 'south':
            for i in range(len(field) - 2, -1, -1):
                for j in range(len(field[i])):
                    if field[i][j] == 'O':
                        for k in range(0, len(field) - i - 1):
                            if field[i + k + 1][j] == '.':
                                field[i + k + 1][j], field[i + k][j] = field[i + k][j], field[i + k + 1][j]
                            else:
                                break
        if direction == 'west':
            for j in range(1, len(field[0])):
                for i in range(len(field)):
                    if field[i][j] == 'O':
                        for k in range(0, j):
                            if field[i][j - k - 1] == '.':
                                field[i][j - k - 1], field[i][j - k] = field[i][j - k], field[i][j - k - 1]
                            else:
                                break
        if direction == 'east':
            for j in range(len(field[0]) - 2, -1, -1):
                for i in range(len(field)):
                    if field[i][j] == 'O':
                        for k in range(0, len(field[0]) - j - 1):
                            if field[i][j + k + 1] == '.':
                                field[i][j + k + 1], field[i][j + k] = field[i][j + k], field[i][j + k + 1]
                            else:
                                break

    load = 0
    for i in range(len(field) - 1, -1, -1):
        multiplier = len(field) - i
        load += len([c for c in field[i] if c == 'O']) * multiplier

    hash1 = hash(';'.join([str(line) for line in field]) + direction)
    # hash1 = ';'.join([str(line) for line in field]) + direction
    # print(cycle, hash1)

    if prev_hash in cache and cache[prev_hash]["next"] is None:
        cache[prev_hash]["next"] = hash1
    if hash1 not in cache:
        cache[hash1] = {"next": None, "load": load}

print(cache[hash1]['load'])
