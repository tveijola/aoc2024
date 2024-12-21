from dataclasses import dataclass, field
import queue

day = "day18"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [tuple(map(int ,line.split(","))) for line in f.read().split("\n")]
    
@dataclass(frozen=True)
class Dir:
    r: int
    c: int

@dataclass(frozen=True)
class Ele:
    r: int
    c: int

@dataclass(order=True)
class PrioItem:
    priority: int
    item: Ele=field(compare=False)

UP = Dir(-1, 0)
RI = Dir(0, 1)
DO = Dir(1, 0)
LE = Dir(0, -1) 
DIRECTIONS = [UP, RI, DO, LE]

# MAX_ROW = 6
# MAX_COL = 6
MAX_ROW = 70
MAX_COL = 70

def manh_dist(pos: Ele, goal: Ele):
    return abs(pos.r - goal.r) + abs(pos.c - goal.c)

def is_inbounds(node: Ele):
    return 0 <= node.r <= MAX_ROW and 0 <= node.c <= MAX_COL

def can_move(pos: Ele, maze: list[list[str]]):
    return is_inbounds(pos) and maze[pos.c][pos.r] == "."

def options(node: Ele, maze: list[list[str]]):
    options = []
    for direction in DIRECTIONS:
        next_pos = Ele(node.r + direction.r, node.c + direction.c)
        if can_move(next_pos, maze):
            options.append((next_pos, 1))
    return options
        

def a_star(start: Ele, goal: Ele, maze: list[list[str]]):
    nodes: queue.PriorityQueue[PrioItem] = queue.PriorityQueue()
    nodes.put(PrioItem(0, start))
    cost_so_far = {}
    cost_so_far[start] = 0
    while not nodes.empty():
        current = nodes.get()
        node = current.item
        if (node.r == goal.r and node.c == goal.c):
            print(f"Goal, cost={cost_so_far[node]}")
            break
        for opt, cost in options(node, maze):
            new_cost = cost_so_far[node] + cost
            if opt not in cost_so_far or new_cost < cost_so_far[opt]:
                cost_so_far[opt] = new_cost
                prio = new_cost + manh_dist(opt, goal)
                nodes.put(PrioItem(prio, opt))

matrix = [["." for _ in range(MAX_COL + 1)] for _ in range(MAX_ROW + 1)]

for i in range(1024):
    col, row = puzzle_input[i]
    matrix[row][col] = "#"
    
a_star(Ele(0, 0), Ele(MAX_ROW, MAX_COL), matrix)