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

visited = set()
start = (-1, -1)
curr_dir = UP

def map_slice(pos: tuple[int, int], dire: tuple[int, int]):
    row, col = pos
    if dire == UP:
        # full_column = [puzzle_input[i][col] for i in range(MAX_COL + 1)]
        column = [puzzle_input[i][col] for i in range(row)]
        return "".join(reversed(column))
    if dire == DO:
        column = [puzzle_input[i][col] for i in range(row + 1, MAX_COL + 1)]
        return "".join(column)
    if dire == LE:
        return "".join(reversed(puzzle_input[row][:col]))
    if dire == RI:
        return "".join(puzzle_input[row][col + 1:])

def next_pos(pos: tuple[int, int], dire: tuple[int, int], steps: int):
    return pos[0] + steps * dire[0], pos[1] + steps * dire[1] 

def find_obstacle(pos: tuple[int, int], dire: tuple[int, int]):
    # how many steps we can take to land just before the obstacle
    line = map_slice(pos, dire)
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
            visited.add((i, pos[1]))
    if col_min != col_max:
        for i in range(col_min, col_max + 1):
            visited.add((pos[0], i))

def travel(pos: tuple[int, int], dire: tuple[int, int]):
    while True:
        steps, found_obs = find_obstacle(pos, dire)
        new_pos = next_pos(pos, dire, steps)
        print(f"travel from {pos} to {new_pos}")
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
visited.add(start)
travel(start, UP)
print(len(visited))