import fileinput

sum_hash = 0
boxes: list[list[tuple[str, int]]] = [[] for i in range(256)]


def print_boxes():
    for i, box in enumerate(boxes):
        if len(box) == 0:
            continue
        print("Box {}: ".format(i), end="")
        for lens in box:
            print("[{} {}] ".format(lens[0], lens[1]), end="")
        print()
    print()


with (fileinput.input(files=("input"), encoding="utf-8") as f):
    res_hash = 0
    label = ""
    for line in f:
        for c in line:
            if c == '=':
                continue
            if '0' <= c <= '9':
                updated = False
                for i, _ in enumerate(boxes[res_hash]):
                    if boxes[res_hash][i][0] == label:
                        boxes[res_hash][i] = (label, int(c))
                        updated = True
                        break
                if not updated:
                    boxes[res_hash].append((label, int(c)))

                # print("After \"{}={}\":".format(label, c))
                # print_boxes()
            if c == '-':
                for i, _ in enumerate(boxes[res_hash]):
                    if boxes[res_hash][i][0] == label:
                        boxes[res_hash].pop(i)
                        break

                # print("After \"{}-\":".format(label))
                # print_boxes()
            if c == ',' or c == '\n':
                res_hash = 0
                label = ""
                continue

            label += c
            res_hash = (res_hash + ord(c)) * 17 % 256

focal_sum = 0
for i, lenses in enumerate(boxes):
    for j, lens in enumerate(lenses):
        focal_sum += (i + 1) * (j + 1) * lens[1]
print(focal_sum)