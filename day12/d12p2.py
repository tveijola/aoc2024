day = "day12"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

visited = []
MAX_ROW = len(puzzle_input) - 1
MAX_COL = len(puzzle_input[0]) - 1
to_visit = []
for i in range(MAX_ROW + 1):
    for j in range(MAX_COL + 1):
        to_visit.append((i, j))

UP = (-1, 0)
RI = (0, 1)
DO = (1, 0)
LE = (0, -1)

def inbounds(coord):
    return 0 <= coord[0] <= MAX_ROW and 0 <= coord[1] <= MAX_COL

def get_neighbors(coord: tuple[int, int]):
    row, col = coord
    above = (row - 1, col)
    right = (row, col + 1)
    below = (row + 1, col)
    left = (row, col - 1)
    return list(filter(lambda coord: inbounds(coord), [above, right, below, left]))

def move_forward(coord, direction):
    return coord[0] + direction[0], coord[1] + direction[1]

def new_direction(direction, turn):
    if turn == LE:
        if direction == UP:
            return LE
        if direction == RI:
            return UP
        if direction == DO:
            return RI
        if direction == LE:
            return DO
    if turn == RI:
        if direction == UP:
            return RI
        if direction == RI:
            return DO
        if direction == DO:
            return LE
        if direction == LE:
            return UP

def is_node_on_right(pos, direction, region):
    if direction == UP:
        return (pos[0], pos[1] + 1) in region
    if direction == RI:
        return (pos[0] + 1, pos[1]) in region
    if direction == DO:
        return (pos[0], pos[1] - 1) in region
    if direction == LE:
        return (pos[0] - 1, pos[1]) in region

def is_node_in_front(pos, direction, region):
    return (pos[0] + direction[0], pos[1] + direction[1]) in region

def calc_perimeter(region: list[tuple[int, int]]):
    start = region[0]
    current = (start[0] - 1, start[1])
    direction = RI
    perim_visited = []
    perim = 0
    while True:
        if (current, direction) in perim_visited:
            break
        perim_visited.append((current, direction))
        on_right = is_node_on_right(current, direction, region)
        in_front = is_node_in_front(current, direction, region)
        if on_right and in_front:
            # need to turn left
            perim += 1
            direction = new_direction(direction, LE)
        elif on_right and not in_front:
            # need to move forward one space
            current = move_forward(current, direction)
        elif (not on_right and in_front) or (not on_right and not in_front):
            # turn right and move one space forward
            perim += 1
            direction = new_direction(direction, RI)
            current = move_forward(current, direction)
    return perim

def resolve_region(coord):
    region_plant = puzzle_input[coord[0]][coord[1]]
    plots_to_check = [coord]
    region = []
    while len(plots_to_check) > 0:
        plot = plots_to_check.pop()
        plant = puzzle_input[plot[0]][plot[1]]
        if plot in region or plant != region_plant:
            continue
        region.append(plot)
        to_visit.remove(plot)
        plots_to_check.extend(get_neighbors(plot))
    return region

def boundaries(region):
    min_row = min(region, key=lambda c: c[0])[0]
    max_row = max(region, key=lambda c: c[0])[0]
    min_col = min(region, key=lambda c: c[1])[1]
    max_col = max(region, key=lambda c: c[1])[1]
    return (min_row, max_row, min_col, max_col)

def region_within_region(region, other_region):
    region_bounds = boundaries(region)
    other_region_bounds = boundaries(other_region)
    if (
        other_region_bounds[0] > region_bounds[0]
        and other_region_bounds[1] < region_bounds[1]
        and other_region_bounds[2] > region_bounds[2]
        and other_region_bounds[3] < region_bounds[3]
    ):
        for c in other_region:
            neighbors = get_neighbors(c)
            if len(neighbors) < 4 or not all(
                [n in region or n in other_region for n in neighbors]
            ):
                return False
        return True
    return False

regions = []
while len(to_visit) > 0:
    coord = to_visit[0]
    regions.append(resolve_region(coord))

price = []
for region in regions:
    i, j = region[0]
    plant = puzzle_input[i][j]
    area = len(region)
    peri = calc_perimeter(region)
    add_peri = 0
    for other_region in regions:
        if other_region[0] == region[0]:
            continue
        if region_within_region(region, other_region):
            add_peri += calc_perimeter(other_region)
    price.append(area * (peri + add_peri))
print(sum(price))