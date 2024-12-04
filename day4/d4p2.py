day = "day4"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

UP = (-1, 0)
UPRI = (-1, 1)
RI = (0, 1)
DORI = (1, 1)
DO = (1, 0)
DOLE = (1, -1)
LE = (0, -1)
UPLE = (-1, -1)

DIRECTIONS = [UP, UPRI, RI, DORI, DO, DOLE, LE, UPLE]

MAX_ROW = len(puzzle_input) - 1
MAX_COL = len(puzzle_input[0]) - 1

def inbounds(row, col):
    if row < 0 or row > MAX_ROW: return None
    if col < 0 or col > MAX_COL: return None
    return row, col

def next(curr: tuple[int, int], direction: tuple[int, int]):
    nextrow, nextcol = curr[0] + direction[0], curr[1] + direction[1]
    return inbounds(nextrow, nextcol)

def nextchar(nextcoord: tuple[int, int], chars: list[str]):
    if nextcoord is None: return None
    nextrow, nextcol = nextcoord
    return chars[nextrow][nextcol]
    
def isxmas(start: tuple[int, int], chars: list[str]):
    # start is coordinate of A
    uplecoord = next(start, UPLE)
    doricoord = next(start, DORI)
    diag1chars = [nextchar(uplecoord, chars), nextchar(doricoord, chars)]
    diag1 = "S" in diag1chars and "M" in diag1chars

    upricoord = next(start, UPRI)
    dolecoord = next(start, DOLE)
    diag2chars = [nextchar(upricoord, chars), nextchar(dolecoord, chars)]
    diag2 = "S" in diag2chars and "M" in diag2chars

    return diag1 and diag2

total = 0
for i in range(MAX_ROW + 1):
    for j in range(MAX_COL + 1):
        char = puzzle_input[i][j]
        if char == "A":
            print(f"found A at {i},{j}")
            if isxmas((i, j), puzzle_input):
                print(f"found xmas at {i},{j}")
                total += 1

print(total)

