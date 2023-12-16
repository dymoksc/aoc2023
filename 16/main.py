import fileinput
from copy import copy

field: list[list[str]] = []
with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for line in f:
        field.append(list(line.rstrip('\n')))
energy_field: list[list[list[str]]] = [[[] for _ in field[0]] for _ in field]


class Beam:
    def __init__(self, row: int, col: int, dir: str):
        self.row = row
        self.col = col
        self.dir = dir


beams: list[Beam] = [Beam(0, -1, '>')]

while len(beams) != 0:
    beam = beams.pop(0)
    if beam.dir == '>':
        beam.col += 1
    elif beam.dir == '<':
        beam.col -= 1
    elif beam.dir == 'v':
        beam.row += 1
    elif beam.dir == '^':
        beam.row -= 1

    if 0 <= beam.row < len(field) and 0 <= beam.col < len(field[0]):
        if beam.dir in energy_field[beam.row][beam.col]:
            continue
        energy_field[beam.row][beam.col].append(beam.dir)
        if field[beam.row][beam.col] == '.':
            beams.append(beam)
        elif field[beam.row][beam.col] == '\\':
            if beam.dir == '>':
                beam.dir = 'v'
            elif beam.dir == '<':
                beam.dir = '^'
            elif beam.dir == 'v':
                beam.dir = '>'
            elif beam.dir == '^':
                beam.dir = '<'
            beams.append(beam)
        elif field[beam.row][beam.col] == '/':
            if beam.dir == '>':
                beam.dir = '^'
            elif beam.dir == '<':
                beam.dir = 'v'
            elif beam.dir == 'v':
                beam.dir = '<'
            elif beam.dir == '^':
                beam.dir = '>'
            beams.append(beam)
        elif field[beam.row][beam.col] == '|':
            if beam.dir == '>' or beam.dir == '<':
                beam_copy = copy(beam)
                beam_copy.dir = 'v'
                beams.append(beam_copy)
                beam.dir = '^'
            beams.append(beam)
        elif field[beam.row][beam.col] == '-':
            if beam.dir == '^' or beam.dir == 'v':
                beam_copy = copy(beam)
                beam_copy.dir = '>'
                beams.append(beam_copy)
                beam.dir = '<'
            beams.append(beam)

print(sum([sum([len(directions) != 0 for directions in row]) for row in energy_field]))
