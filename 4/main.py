import fileinput

scratchcards = 0
with fileinput.input(files=('input'), encoding="utf-8") as f:
    next_multiplier = []
    for line in f:
        multiplier = len(next_multiplier) + 1
        next_multiplier = [i - 1 for i in next_multiplier if i > 1]

        card, numbers = line.split(": ")
        winning_numbers, actual_numbers = numbers.split(" | ")
        winning_numbers = [int(i) for i in winning_numbers.strip(" \n").split()]
        actual_numbers = [int(i) for i in actual_numbers.strip(" \n").split()]
        matches = sum(1 for i in actual_numbers if i in winning_numbers)
        if matches != 0:
            for i in range(multiplier):
                next_multiplier.append(matches)
        print("{}: {} match(es) x {}, gives {} multiplier".format(card, matches, multiplier, next_multiplier))
        scratchcards += multiplier
print("{} scratchcards".format(scratchcards))