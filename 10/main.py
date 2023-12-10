import fileinput

tiles: list[list[str]] = []
i = 0
dist: dict[tuple[int, int], int] = {}
prev: dict[tuple[int, int], tuple[int, int]] = {}
is_in_q: dict[tuple[int, int], bool] = {}
q: list[tuple[int, int]] = []
neighbors: list[list[list[tuple[int, int]]]] = []

with fileinput.input(files=("input"), encoding="utf-8") as f:
    for l in f:
        neighbors.append([])
        tiles.append(list(l.rstrip("\n")))
        for j in range(len(tiles[i])):
            neighbors[i].append([])
            if tiles[i][j] == "S":
                start = (i, j)
            elif tiles[i][j] == "-":
                neighbors[i][j].append((i, j - 1))
                neighbors[i][j].append((i, j + 1))
            elif tiles[i][j] == "|":
                neighbors[i][j].append((i - 1, j))
                neighbors[i][j].append((i + 1, j))
            elif tiles[i][j] == "F":
                neighbors[i][j].append((i, j + 1))
                neighbors[i][j].append((i + 1, j))
            elif tiles[i][j] == "7":
                neighbors[i][j].append((i, j - 1))
                neighbors[i][j].append((i + 1, j))
            elif tiles[i][j] == "L":
                neighbors[i][j].append((i, j + 1))
                neighbors[i][j].append((i - 1, j))
            elif tiles[i][j] == "J":
                neighbors[i][j].append((i, j - 1))
                neighbors[i][j].append((i - 1, j))
            dist[(i, j)] = 99999
            prev[(i, j)] = (-1, -1)
            q.append((i, j))
            is_in_q[(i, j)] = True
        i += 1
dist[start] = 0

if start in neighbors[start[0] - 1][start[1]]:
    neighbors[start[0]][start[1]].append((start[0] - 1, start[1]))
if start in neighbors[start[0] + 1][start[1]]:
    neighbors[start[0]][start[1]].append((start[0] + 1, start[1]))
if start in neighbors[start[0]][start[1] - 1]:
    neighbors[start[0]][start[1]].append((start[0], start[1] - 1))
if start in neighbors[start[0]][start[1] + 1]:
    neighbors[start[0]][start[1]].append((start[0], start[1] + 1))

print("cleaning neighbors")
for i in range(len(neighbors)):
    for j in range(len(neighbors[i])):
        neighbors[i][j] = [n for n in neighbors[i][j] if 0 <= n[0] < len(tiles) and 0 <= n[1] < len(tiles[0])]

print("d start")
while len(q) != 0:
    min_dist = 99999
    i_to_pop = -1
    for i in range(len(q)):
        if dist[q[i]] < min_dist:
            min_dist = dist[q[i]]
            i_to_pop = i
    u = q.pop(i_to_pop)
    is_in_q[u] = False
    print(len(q))
    for v in neighbors[u[0]][u[1]]:
        if not is_in_q[v]:
            continue
        alt = dist[u] + 1
        if alt < dist[v]:
            dist[v] = alt
            prev[v] = u
print("d end")

max_dist = 0
for i in range(len(tiles)):
    for j in range(len(tiles[0])):
        if dist[(i, j)] < 99999:
            max_dist = max(max_dist, dist[(i, j)])

# Ray casting
counter = 0
for i in range(len(tiles)):
    enc_walls = 0
    for j in range(len(tiles[0])):
        if dist[(i, j)] == 99999:
            if enc_walls % 2 == 1:
                counter += 1
                tiles[i][j] = "1"
            else:
                tiles[i][j] = "0"
        elif i != len(tiles) - 1 and (i + 1, j) in neighbors[i][j]:
            enc_walls += 1
        elif i == len(tiles) - 1 and (i - 1, j) in neighbors[i][j]:
            enc_walls += 1
        print(tiles[i][j], end="")
    print()

print(counter)

# print(max_dist)
