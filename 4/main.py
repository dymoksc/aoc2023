import fileinput

with fileinput.input(files=('input'), encoding="utf-8") as f:
    points_sum = 0
    for line in f:
        card, numbers = line.split(": ")
        winning_numbers, actual_numbers = numbers.split(" | ")
        winning_numbers = [int(i) for i in winning_numbers.strip(" \n").split()]
        actual_numbers = [int(i) for i in actual_numbers.strip(" \n").split()]
        power = sum(1 for i in actual_numbers if i in winning_numbers) - 1
        points = 0 if power == -1 else pow(2, power)
        print("{}: {} point(s)".format(card, points))
        points_sum += points
    print("Points sum: {}".format(points_sum))