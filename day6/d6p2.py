day = "day6"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split()

print(puzzle_input)

UP = (-1, 0)
RI = (0, 1)
DO = (1, 0)
LE = (0, -1)

DIRECTIONS = [UP, RI, DO, LE]

MAX_ROW = len(puzzle_input) - 1
MAX_COL = len(puzzle_input[0]) - 1

original_route = set()
start = (-1, -1)
curr_dir = UP

def map_slice(pos: tuple[int, int], dire: tuple[int, int], the_map=None):
    row, col = pos
    if the_map is None:
        the_map = puzzle_input
    if dire == UP:
        # full_column = [puzzle_input[i][col] for i in range(MAX_COL + 1)]
        column = [the_map[i][col] for i in range(row)]
        return "".join(reversed(column))
    if dire == DO:
        column = [the_map[i][col] for i in range(row + 1, MAX_COL + 1)]
        return "".join(column)
    if dire == LE:
        return "".join(reversed(the_map[row][:col]))
    if dire == RI:
        return "".join(the_map[row][col + 1:])

def next_pos(pos: tuple[int, int], dire: tuple[int, int], steps: int):
    return pos[0] + steps * dire[0], pos[1] + steps * dire[1] 

def find_obstacle(pos: tuple[int, int], dire: tuple[int, int], the_map=None):
    # how many steps we can take to land just before the obstacle
    line = map_slice(pos, dire, the_map)
    try:
        return line.index("#"), True
    except:
        return len(line), False

def change_dir(dire):
    if dire == UP: return RI
    if dire == RI: return DO
    if dire == DO: return LE
    if dire == LE: return UP

def add_visited(pos: tuple[int, int], next_pos: tuple[int, int]):
    row_min = min(pos[0], next_pos[0])
    row_max = max(pos[0], next_pos[0])
    col_min = min(pos[1], next_pos[1])
    col_max = max(pos[1], next_pos[1])
    if row_min != row_max:
        for i in range(row_min, row_max + 1):
            original_route.add((i, pos[1]))
    if col_min != col_max:
        for i in range(col_min, col_max + 1):
            original_route.add((pos[0], i))

def populate_route(pos: tuple[int, int], dire: tuple[int, int]):
    while True:
        steps, found_obs = find_obstacle(pos, dire)
        new_pos = next_pos(pos, dire, steps)
        add_visited(pos, new_pos)
        if found_obs:
            pos = new_pos
            dire = change_dir(dire)
        else:
            break

for i in range(MAX_ROW + 1):
    if "^" in puzzle_input[i]:
        j = puzzle_input[i].index("^")
        start = (i, j)
        break

print(f"start is {i}, {j}")
populate_route(start, UP)
print(len(original_route))

def get_travel_nodes(pos: tuple[int, int], next_pos: tuple[int, int], dire):
    nodes = set()
    row_min = min(pos[0], next_pos[0])
    row_max = max(pos[0], next_pos[0])
    col_min = min(pos[1], next_pos[1])
    col_max = max(pos[1], next_pos[1])
    if row_min != row_max:
        for i in range(row_min, row_max + 1):
            nodes.add(((i, pos[1]), dire))
    if col_min != col_max:
        for i in range(col_min, col_max + 1):
            nodes.add(((pos[0], i), dire))
    return nodes

def detect_loop(start: tuple[int, int], the_map: list[str]):
    pos = start
    dire = UP
    nodes = set((start, UP))
    while True:
        steps, found_obs = find_obstacle(pos, dire, the_map)
        new_pos = next_pos(pos, dire, steps)
        new_nodes = get_travel_nodes(pos, new_pos, dire)
        intersect = nodes.intersection(new_nodes)
        if (len(intersect) > 0):
            return True # is a loop
        nodes.update(new_nodes)
        if found_obs:
            pos = new_pos
            dire = change_dir(dire)
        else:
            # Got out
            break
    return False

total = 0
for pos in original_route:
    obstructed = puzzle_input.copy()
    row, col = pos
    obstructed[row] = obstructed[row][:col] + "#" + obstructed[row][col + 1:]
    loop = detect_loop(start, obstructed)
    if loop:
        total += 1
        print(f"adding obstruction to {pos} results in a loop")

print(total)