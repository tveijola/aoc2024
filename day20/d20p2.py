from dataclasses import dataclass, field
import queue

day = "day20"

# filename = f"./{day}/sample"
# minimum_save = 50
filename = f"./{day}/data"
minimum_save = 100

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]


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

MAX_ROW = len(puzzle_input) - 1
MAX_COL = len(puzzle_input[0]) - 1

def manh_dist(pos: Ele, goal: Ele):
    return abs(pos.r - goal.r) + abs(pos.c - goal.c)

def can_move(pos: Ele, maze: list[list[str]]):
    return maze[pos.r][pos.c] == "."

def options(node: Ele, maze: list[list[str]]):
    options = []
    for direction in DIRECTIONS:
        next_pos = Ele(node.r + direction.r, node.c + direction.c)
        if can_move(next_pos, maze):
            options.append((next_pos, 1))
    return options

def construct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))

def a_star(start: Ele, goal: Ele, maze: list[list[str]]):
    nodes: queue.PriorityQueue[PrioItem] = queue.PriorityQueue()
    nodes.put(PrioItem(0, start))
    cost_so_far = {}
    cost_so_far[start] = 0
    came_from = {}
    while not nodes.empty():
        current = nodes.get()
        node = current.item
        if (node.r == goal.r and node.c == goal.c):
            return construct_path(came_from, node)
            # print(f"Goal, cost={cost_so_far[node]}")
        for opt, cost in options(node, maze):
            new_cost = cost_so_far[node] + cost
            if opt not in cost_so_far or new_cost < cost_so_far[opt]:
                came_from[opt] = node
                cost_so_far[opt] = new_cost
                prio = new_cost + manh_dist(opt, goal)
                nodes.put(PrioItem(prio, opt))
    return cost_so_far[node]

track: list[list[str]] = []
start = None
goal = None
for i in range(len(puzzle_input)):
    line = puzzle_input[i]
    if "S" in line:
        start = Ele(i, line.index("S"))
        line = line.replace("S", ".")
    if "E" in line:
        goal = Ele(i, line.index("E"))
        line = line.replace("E", ".")
    track.append([c for c in line])
print(start)
print(goal)

path = a_star(start, goal, track)
time_wo_cheats = len(path) - 1

cheated_times = {}
at_least_100 = 0
for i in range(len(path)):
    print(f"{i}/{len(path)-1}")
    node = path[i]
    for cheat in filter(lambda n, goal=node: 2 <= manh_dist(n, goal) <= 20, path[i + minimum_save:]):
        move_time = manh_dist(node, cheat)
        to_idx = path.index(cheat)
        cheated_time = i + move_time + (time_wo_cheats - to_idx)
        saved_time = time_wo_cheats - cheated_time
        if saved_time >= minimum_save:
            at_least_100 += 1
            if saved_time in cheated_times:
                cheated_times[saved_time] += 1
            else: 
                cheated_times[saved_time] = 1

final_times = []
for key, val in cheated_times.items():
    final_times.append((val, key))
final_times.sort(key=lambda v: v[1])
for count, saved_pico in final_times:
    print(f"there are {count} cheats that save {saved_pico} picoseconds")
print(f"total cheats that save at least 100 picoseconds: {at_least_100}")