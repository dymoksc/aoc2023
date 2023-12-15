import fileinput

sum_hash = 0

with (fileinput.input(files=("input"), encoding="utf-8") as f):
    res_hash = 0
    for line in f:
        for c in line:
            if c == ',' or c == '\n':
                # print("- ", res_hash)
                sum_hash += res_hash
                res_hash = 0
                continue

            # print(c, end=" ")
            res_hash = (res_hash + ord(c)) * 17 % 256
            # print(res_hash)

print(sum_hash)