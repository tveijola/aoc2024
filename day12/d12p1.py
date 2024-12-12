day = "day12"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

visited = []
MAX_ROW = len(puzzle_input) - 1
MAX_COL = len(puzzle_input[0]) - 1

def inbounds(coord):
    return 0 <= coord[0] <= MAX_ROW and 0 <= coord[1] <= MAX_COL

def get_neighbors(coord: tuple[int, int]):
    row, col = coord
    above = (row - 1, col)
    right = (row, col + 1)
    below = (row + 1, col)
    left  = (row, col - 1)
    return list(filter(lambda coord: inbounds(coord), [above, right, below, left]))

def calc_perimeter(region: list[tuple[int, int]]):
    perimeter = 0
    for plot in region:
        neighbors = get_neighbors(plot)
        region_neighbors = sum(1 if n in region else 0 for n in neighbors)
        perimeter += 4 - region_neighbors
        # how many neighbors are in the region
    return perimeter
        

def calculate_area(coord):
    if (coord in visited): return 0
    i, j = coord
    ch = puzzle_input[i][j]
    plots_to_check = [coord]
    region = []
    while len(plots_to_check) > 0:
        plot = plots_to_check.pop()
        plant = puzzle_input[plot[0]][plot[1]]
        if plot in region or plant != ch:
            continue
        region.append(plot)
        plots_to_check.extend(get_neighbors(plot))
    visited.extend(region)
    return len(region) * calc_perimeter(region)

total = 0
for i in range(MAX_ROW + 1):
    for j in range(MAX_COL + 1):
        if (i, j) not in visited:
            total += calculate_area((i, j))
print(total)