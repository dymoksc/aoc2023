import fileinput
from enum import Enum


class CardType(Enum):
    five_of_a_kind = 6
    four_of_a_kind = 5
    full_house = 4
    three_of_a_kind = 3
    two_pair = 2
    one_pair = 1
    high_card = 0

labels = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
label_inter_map = {c: len(labels) - i for i, c in enumerate(labels)}

# Load cards w finding there type O(n)
cards = []
with fileinput.input(files=('input'), encoding="utf-8") as f:
    for line in f:
        card, bidding = line.split()
        label_freq = {l: 0 for l in labels}
        card_type = CardType.high_card
        label_inter = []
        jokers = 0
        for l in card:
            label_inter.append(label_inter_map[l])
            if l == 'J':
                jokers += 1
                continue
            label_freq[l] += 1
            if label_freq[l] == 2:
                if card_type == CardType.high_card:
                    card_type = CardType.one_pair
                elif card_type == CardType.one_pair:
                    card_type = CardType.two_pair
                elif card_type == CardType.three_of_a_kind:
                    card_type = CardType.full_house
            elif label_freq[l] == 3:
                if card_type == CardType.one_pair:
                    card_type = CardType.three_of_a_kind
                elif card_type == CardType.two_pair:
                    card_type = CardType.full_house
            elif label_freq[l] == 4:
                card_type = CardType.four_of_a_kind
            elif label_freq[l] == 5:
                card_type = CardType.five_of_a_kind

        while jokers != 0:
            if card_type == CardType.high_card:
                card_type = CardType.one_pair
            elif card_type == CardType.one_pair:
                card_type = CardType.three_of_a_kind
            elif card_type == CardType.two_pair:
                card_type = CardType.full_house
            elif card_type == CardType.three_of_a_kind:
                card_type = CardType.four_of_a_kind
            elif card_type == CardType.four_of_a_kind:
                card_type = CardType.five_of_a_kind
            jokers -= 1

        cards.append((card, int(bidding), card_type, label_inter, [card_type.value] + label_inter))

# Sort by type and first card O(log(n)) * 5
cards.sort(key=lambda t: t[4])

# Sum biddings O(n)
s = sum(card[1] * (i + 1) for i, card in enumerate(cards))
print(s)
