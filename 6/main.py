# s = h * (t - h) = h * t - h^2
import fileinput
import math

# h = 0
# s = 0 * (7 - 0) = 0

# h = 1
# s = 1 * (7 - 1) = 6

# h = 2
# s = 2 * (7 - 2) = 10

# h * t - h > s
# 7h - h > 9
# 6h > 9
# h > 9/6
# h > 1,5

# 7 - 2 = 5.5

# 15h - h^2 > 40
# h^2 - 15h + 40 = 0
# d = 225 - 160 = 65
# h = (15 +- sqrt(65)) / 2 = (15 +- 8) / 2 = 11.53, 3.5

with fileinput.input(files=('input'), encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 0:
            assert line.split(":")[0] == "Time"
            times = [int(i) for i in line.split(":")[1].strip().split()]
            print(times)
        elif i == 1:
            assert line.split(":")[0] == "Distance"
            distances = [int(i) for i in line.split(":")[1].strip().split()]
            print(distances)
        else:
            assert False

ans = 1
for i in range(len(times)):
    # x^2 - times[0] * x + distances[0] = 0
    d = times[i] * times[i] - 4 * 1 * distances[i]
    x1 = (times[i] - math.sqrt(d)) / 2
    # x2 = (times[i] + math.sqrt(d)) / 2

    # print(x1, x2)
    print(math.floor(x1) + 1, times[i] - (math.floor(x1) + 1))
    # print(times[i] - 2 * math.floor(x1) - 1)
    ways = times[i] - 2 * math.floor(x1) - 1
    ans *= ways
    # print(math.floor(x2) + 1 - (math.floor(x1) - 1))

    # min_time_pressed = distances[i] / (times[i] - 1)
    # max_time_pressed = times[i] - min_time_pressed
    # print(math.ceil(min_time_pressed), math.ceil(max_time_pressed))
    # ways = math.ceil(max_time_pressed) - math.ceil(min_time_pressed)
    # print(ways)

print(ans)