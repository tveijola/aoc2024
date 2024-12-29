from dataclasses import dataclass
from functools import cache
from typing import Optional

@dataclass(frozen=True)
class Ele:
    r: int
    c: int

@dataclass(frozen=True)
class Dir:
    r: int
    c: int

    def __repr__(self):
        if self.r == -1 and self.c == 0: return "^"
        if self.r == 0 and self.c == 1: return ">"
        if self.r == 1 and self.c == 0: return "v"
        if self.r == 0 and self.c == -1: return "<"

UP = Dir(-1, 0)
RI = Dir(0, 1)
DO = Dir(1, 0)
LE = Dir(0, -1) 

numpad = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    [None, 0, "A"],
]

keypad = [
    [None, UP, "A"],
    [LE, DO, RI],
]

MAX_DEPTH = 26

@cache
def get_keypad_directions(start: Ele, goal: Ele):
    res = []
    if start == goal:
        return res
    rows = goal.r - start.r
    cols = goal.c - start.c
    if start.c == 0 and goal.r == 0:
        if cols > 0:
            res.extend([RI for _ in range(abs(cols))])
        if rows < 0:
            res.extend([UP for _ in range(abs(rows))])
    elif goal.c == 0 and start.r == 0:
        if rows > 0:
            res.extend([DO for _ in range(abs(rows))])
        if cols < 0:
            res.extend([LE for _ in range(abs(cols))])
    else:
        if cols < 0:
            res.extend([LE for _ in range(abs(cols))])
        if rows > 0:
            res.extend([DO for _ in range(abs(rows))])
        if rows < 0:
            res.extend([UP for _ in range(abs(rows))])
        if cols > 0:
            res.extend([RI for _ in range(abs(cols))])
    return res


def get_numpad_directions(start: Ele, goal: Ele):
    res = []
    if start == goal:
        return res
    rows = goal.r - start.r
    cols = goal.c - start.c
    if start.c == 0 and goal.r == 3:
        if cols > 0:
            res.extend([RI for _ in range(abs(cols))])
        if rows > 0:
            res.extend([DO for _ in range(abs(rows))])
    elif goal.c == 0 and start.r == 3:
        if rows < 0:
            res.extend([UP for _ in range(abs(rows))])
        if cols < 0:
            res.extend([LE for _ in range(abs(cols))])
    else: 
        if cols < 0:
            res.extend([LE for _ in range(abs(cols))])
        if rows > 0:
            res.extend([DO for _ in range(abs(rows))])
        if rows < 0:
            res.extend([UP for _ in range(abs(rows))])
        if cols > 0:
            res.extend([RI for _ in range(abs(cols))])
    return res

@cache
def find_item(item):
    for i in range(len(keypad)):
        row = keypad[i]
        if item in row:
            return Ele(i, row.index(item))

@cache
def get_presses(moves: tuple[Dir], depth):
    if depth == MAX_DEPTH:
        # human operator
        return len(moves) + 1
    result = 0
    pos = Ele(0, 2)
    for move in moves + ("A",):
        goal = find_item(move)
        next_depth_moves = get_keypad_directions(pos, goal)
        result += get_presses(tuple(next_depth_moves), depth + 1)
        pos = goal
    return result

day = "day21"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

def find_numpad_item(item):
    for i in range(len(numpad)):
        row = numpad[i]
        if item in row:
            return Ele(i, row.index(item))

total_complexity = 0
for combination in puzzle_input:
    pos = Ele(3, 2)
    presses = 0
    for c in combination:
        c = int(c) if c.isnumeric() else c
        goal = find_numpad_item(c)
        directions = get_numpad_directions(pos, goal)
        pos = goal
        presses += get_presses(tuple(directions), 1)
    char_list = [c for c in combination]
    numeric_code = int("".join(filter(lambda c: c.isnumeric(), char_list)))
    print(f"{presses} * {numeric_code}")
    total_complexity += numeric_code * presses
print(total_complexity)
