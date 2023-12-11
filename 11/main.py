import fileinput

expansion = 1000000

galaxies_by_col: dict[int, list[tuple[int, int]]] = {}
cols = 0
rows = 0

with fileinput.input(files=("input"), encoding="utf-8") as f:
    for line in f:
        rows += 1
        galaxies_in_row = 0
        for j, c in enumerate(line):
            if c == "#":
                galaxies_in_row += 1
                if j not in galaxies_by_col:
                    galaxies_by_col[j] = []
                galaxies_by_col[j].append((rows - 1, j))
        if galaxies_in_row == 0:
            rows += expansion - 1
        cols = j + 1

last_row_w_galaxy = -1
modifier = 0
all_galaxies: list[tuple[int, int]] = []
galaxies_by_col = dict(sorted(galaxies_by_col.items()))
for k, galaxies in galaxies_by_col.items():
    modifier += (k + modifier - last_row_w_galaxy - 1) * (expansion - 1)
    k += modifier
    last_row_w_galaxy = k
    for galaxy in galaxies:
        all_galaxies.append((galaxy[0], k))
cols += modifier

sum = 0
for i in range(len(all_galaxies)):
    for j in range(i, len(all_galaxies)):
        sum += abs(all_galaxies[i][0] - all_galaxies[j][0])
        sum += abs(all_galaxies[i][1] - all_galaxies[j][1])

# for i in range(rows):
#     for j in range(cols):
#         if (i, j) in all_galaxies:
#             print("#", end="")
#         else:
#             print(".", end="")
#     print()

print(sum)