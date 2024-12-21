from dataclasses import dataclass, field
import queue

day = "day20"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

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

def a_star(start: Ele, goal: Ele, maze: list[list[str]]):
    nodes: queue.PriorityQueue[PrioItem] = queue.PriorityQueue()
    nodes.put(PrioItem(0, start))
    cost_so_far = {}
    cost_so_far[start] = 0
    while not nodes.empty():
        current = nodes.get()
        node = current.item
        if (node.r == goal.r and node.c == goal.c):
            # print(f"Goal, cost={cost_so_far[node]}")
            break
        for opt, cost in options(node, maze):
            new_cost = cost_so_far[node] + cost
            if opt not in cost_so_far or new_cost < cost_so_far[opt]:
                cost_so_far[opt] = new_cost
                prio = new_cost + manh_dist(opt, goal)
                nodes.put(PrioItem(prio, opt))
    return cost_so_far[node]

def horiz_cheat(node, track):
    left = track[node.r + LE.r][node.c + LE.c]
    right = track[node.r + RI.r][node.c + RI.c]
    return left == "." and right == "."

def verti_cheat(node, track):
    above = track[node.r + UP.r][node.c + UP.c]
    below = track[node.r + DO.r][node.c + DO.c]
    return above == "." and below == "."

def can_cheat(node: Ele, track: list[list[str]]):
    char = track[node.r][node.c]
    if char != "#":
        return False
    return horiz_cheat(node, track) or verti_cheat(node, track)
    

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
time_wo_cheats = a_star(start, goal, track)

at_least_100 = 0
cheats = {}
for i in range(1, len(track) - 1):
    for j in range(1, len(track[0]) - 1):
        if (can_cheat(Ele(i, j), track)):
            print(f"cheating at {i, j}")
            cheat_track = [[c for c in line] for line in track]
            cheat_track[i][j] = "."
            time_with_cheat = a_star(start, goal, cheat_track)
            saved_time = time_wo_cheats - time_with_cheat
            if saved_time > 0:
                if saved_time >= 100:
                    at_least_100 += 1
                if saved_time in cheats:
                    cheats[saved_time] += 1
                else:
                    cheats[saved_time] = 1
for key, val in cheats.items():
    print(f"there are {val} cheats that save {key} picoseconds")
print("at least 100: ", at_least_100)