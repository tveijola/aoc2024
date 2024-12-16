from dataclasses import dataclass, field
import math
import queue

day = "day16"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

        
@dataclass
class Dir:
    r: int
    c: int
    def __hash__(self):
        return hash(self.r) + hash(self.c)

@dataclass
class Ele:
    r: int
    c: int
    d: str
    def __hash__(self):
        return hash(self.r) + hash(self.c) + hash(self.d)

@dataclass(order=True)
class PrioItem:
    priority: int
    item: Ele=field(compare=False)

UP = Dir(-1, 0)
RI = Dir(0, 1)
DO = Dir(1, 0)
LE = Dir(0, -1)

start = Ele(0, 0, ">")
goal = Ele(0, 0, "E")
maze: list[list[Ele]] = []
for i in range(len(puzzle_input)):
    row = []
    for j in range(len(puzzle_input[i])):
        data = puzzle_input[i][j]
        if data == "S":
            start.r = i
            start.c = j
        if data == "E":
            goal.r = i
            goal.c = j
        row.append(Ele(i, j, data))
    maze.append(row)


def get_dir(pos: Ele):
    if pos.d == ">": return RI
    if pos.d == "<": return LE
    if pos.d == "^": return UP
    if pos.d == "v": return DO

def manh_dist(pos: Ele, goal: Ele):
    return abs(pos.r - goal.r) + abs(pos.c - goal.c)

def get_next_pos(pos: Ele, direction: Dir) -> Ele:
    row = pos.r + direction.r
    col = pos.c + direction.c
    return Ele(row, col, pos.d)

def get_data(pos: Ele, maze: list[list[Ele]], direction: Dir):
    return maze[pos.r + direction.r][pos.c + direction.c].d

def get_possible_directions(direction: Dir):
    if direction in [UP, DO]: return ["<", ">"]
    if direction in [LE, RI]: return ["^", "v"]
    

def options(pos: Ele, maze: list[list[Ele]]):
    direction = get_dir(pos)
    next_data = get_data(pos, maze, direction)
    opts: list[Ele] = []
    if (next_data != "#"):
        opts.append((get_next_pos(pos, direction), 1))
    for new_dir in get_possible_directions(direction):
        el = Ele(pos.r, pos.c, new_dir)
        possible_dir = get_dir(el)
        possible_data = get_data(el, maze, possible_dir)
        if possible_data != "#": # skip directions that would face the wall
            opts.append((el, 1000))
    return opts


def a_star(start: Ele, goal: Ele, maze: list[list[Ele]]):
    nodes: queue.PriorityQueue[PrioItem] = queue.PriorityQueue()
    nodes.put(PrioItem(0, start))
    cost_so_far = {}
    cost_so_far[start] = 0
    while not nodes.empty():
        current = nodes.get()
        node = current.item
        # print(f"current: {node}")
        if (node.r == goal.r and node.c == goal.c):
            print(f"Goal, cost={cost_so_far[node]}")
            break
        for opt, cost in options(node, maze):
            new_cost = cost_so_far[node] + cost
            if opt not in cost_so_far or new_cost < cost_so_far[opt]:
                cost_so_far[opt] = new_cost
                prio = new_cost + manh_dist(opt, goal)
                nodes.put(PrioItem(prio, opt))

res = a_star(start, goal, maze)