from itertools import combinations

day = "day8"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split()

MAX_ROW = len(puzzle_input) - 1
MAX_COL = len(puzzle_input[0]) - 1

def inbounds(coord):
    i, j = coord
    return i >= 0 and i <= MAX_ROW and j >= 0 and j <= MAX_COL

antennas: dict[str, list[tuple[int, int]]] = {}
for i in range(MAX_ROW + 1):
    for j in range(MAX_COL + 1):
        c = puzzle_input[i][j]
        if c != ".":
            if c in antennas: antennas.get(c).append((i, j))
            else: antennas[c] = [(i, j)]

antinodes = set()
for val in antennas.values():
    for pair in combinations(val, 2):
        a1, a2 = pair
        i, j = a2[0] - a1[0], a2[1] - a1[1] # vector i, j
        an1 = a1[0] - i, a1[1] - j
        an2 = a2[0] + i, a2[1] + j
        if inbounds(an1): antinodes.add(an1)
        if inbounds(an2): antinodes.add(an2)
print(len(antinodes))