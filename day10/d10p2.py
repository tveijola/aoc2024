day = "day10"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [list(map(int, line.strip())) for line in f.readlines()]
ROW_MAX = len(puzzle_input) - 1
COL_MAX = len(puzzle_input[0]) - 1

def is_inbounds(coord: tuple[int, int]):
    row, col = coord
    return 0 <= row <= ROW_MAX and 0 <= col <= COL_MAX

def get_neighbor_coords(coord: tuple[int, int]):
    row, col = coord
    above = (row - 1, col)
    right = (row, col + 1)
    below = (row + 1, col)
    left  = (row, col - 1)
    return list(filter(lambda coord: is_inbounds(coord), [above, right, below, left]))

def calculate_score(trailhead: tuple[int, int], topo: list[list[int]]):
    nodes = [(trailhead, 0)]
    score = 0
    while len(nodes) > 0:
        this_node = nodes.pop(0)
        this_coord, this_height = this_node
        if this_height == 9:
            score += 1
            continue # found highest point
        neighbor_coords = get_neighbor_coords(this_coord)
        for n_coord in neighbor_coords:
            neighbor_height = topo[n_coord[0]][n_coord[1]]
            if neighbor_height - this_height == 1:
                nodes.append((n_coord, neighbor_height))
    return score
    
total = 0
for i in range(ROW_MAX + 1):
    for j in range(COL_MAX + 1):
        height = puzzle_input[i][j]
        if height == 0:
            total += calculate_score((i, j), puzzle_input)
print(total)