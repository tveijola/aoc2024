from dataclasses import dataclass
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
        if cols > 0:
            res.extend([RI for _ in range(abs(cols))])
        if rows < 0:
            res.extend([UP for _ in range(abs(rows))])
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
        if cols > 0:
            res.extend([RI for _ in range(abs(cols))])
        if rows < 0:
            res.extend([UP for _ in range(abs(rows))])
    return res

def get_pad_directions(start: Ele, goal: Ele, is_numpad: bool):
    if is_numpad:
        return get_numpad_directions(start, goal)
    return get_keypad_directions(start, goal)

class Actor():
    def __init__(self, pos: Ele, pad: list[list], name: str, is_numpad: bool):
        self.pos = pos
        self.operator: Optional[Actor] = None
        self.operand: Optional[Actor] = None
        self.pad = pad
        self.name = name
        self.presses = []
        self.is_numpad = is_numpad

    def set_operator(self, operator):
        self.operator: Actor = operator

    def set_operand(self, operator):
        self.operand: Actor = operator

    # request move in direction from operator
    def request_move(self, direction: Dir):
        self.operator.move_to_button_and_press(direction)
        self.pos = self.next_pos(direction)
        
    # request activation from operator
    def request_activate(self):
        # print(f"actor {self.name} request activation")
        self.operator.move_to_button_and_press("A")
    
    def find_item(self, item):
        for i in range(len(self.pad)):
            row = self.pad[i]
            if item in row:
                return Ele(i, row.index(item))

    def move(self, item):
        goal = self.find_item(item)
        moves = get_pad_directions(self.pos, goal, self.is_numpad)
        for move in moves:
            # print(f"actor {self.name} request move {move}")
            self.request_move(move)
    
    def move_to_button_and_press(self, item):
        if self.operator is None:
            self.presses.append(str(item))
        else:
            self.move(item)
            self.request_activate()

    def next_pos(self, direction: Dir):
        return Ele(self.pos.r + direction.r, self.pos.c + direction.c)

class KeypadActor(Actor):
    def __init__(self, name: str):
        super().__init__(Ele(0, 2), keypad, name, False)

class NumpadActor(Actor):
    def __init__(self, name: str):
        super().__init__(Ele(3, 2), numpad, name, True)
    
day = "day21"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

me = KeypadActor("me")
k1 = KeypadActor("k1")
k2 = KeypadActor("k2")
nr = NumpadActor("nr")
me.set_operand(k1)
k1.set_operator(me)
k1.set_operand(k2)
k2.set_operator(k1)
k2.set_operand(nr)
nr.set_operator(k2)

total_complexity = 0
for combination in puzzle_input:
    me.presses.clear()
    for c in combination:
        c = int(c) if c.isnumeric() else c
        nr.move_to_button_and_press(c)
    char_list = [c for c in combination]
    numeric_code = int("".join(filter(lambda c: c.isnumeric(), char_list)))
    print(f"{len(me.presses)} * {numeric_code}")
    total_complexity += numeric_code * len(me.presses)
    print("".join(me.presses))

print(total_complexity)