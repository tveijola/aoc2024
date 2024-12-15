import re


day = "day15"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split("\n\n")

UP = (-1, 0)
RI = (0, 1)
DO = (1, 0)
LE = (0, -1)


def get_dir(move_char: str):
    if move_char == "^":
        return UP
    if move_char == "<":
        return LE
    if move_char == ">":
        return RI
    if move_char == "v":
        return DO


def is_empty(coord: tuple[int, int], warehouse: list[list[str]]):
    return warehouse[coord[0]][coord[1]] == "."


def is_wall(coord: tuple[int, int], warehouse: list[list[str]]):
    return warehouse[coord[0]][coord[1]] == "#"


def is_box(coord: tuple[int, int], warehouse: list[list[str]]):
    return warehouse[coord[0]][coord[1]] in "[]"


def get_obj(coord: tuple[int, int], warehouse: list[list[str]]):
    return warehouse[coord[0]][coord[1]]


def resolve_boxes(
    warehouse: list[list[str]], current: tuple[int, int], direction: tuple[int, int]
):
    next_pos = current[0] + direction[0], current[1] + direction[1]
    obj = get_obj(next_pos, warehouse)
    if obj == "#":
        return False
    elif obj == ".":
        return [current]
    if obj == "[":
        next_left_pos = next_pos
        next_right_pos = next_pos[0], next_pos[1] + 1
    else:
        next_right_pos = next_pos
        next_left_pos = next_pos[0], next_pos[1] - 1
    box_left = resolve_boxes(warehouse, next_left_pos, direction)
    box_right = resolve_boxes(warehouse, next_right_pos, direction)
    if box_left is False or box_right is False:
        return False
    res = [current]
    for box in box_left:
        res.append(box)
    for box in box_right:
        res.append(box)
    return res


def move_up_or_down(warehouse: list[list[str]], box: tuple[int, int], direction: int):
    obj = get_obj(box, warehouse)
    new_pos = box[0] + direction, box[1]
    warehouse[new_pos[0]][new_pos[1]] = obj
    warehouse[box[0]][box[1]] = "."
    return warehouse


def move_boxes_horizontal(
    warehouse: list[list[str]],
    robot: tuple[int, int],
    next_pos: tuple[int, int],
    direction: tuple[int, int],
):
    row = "".join(warehouse[robot[0]])
    new_row = row[: robot[1]] if direction == LE else row[robot[1] + 1 :]
    if "." not in new_row:
        return robot, warehouse  # cannot move
    if direction == LE:
        if new_row.rfind("#") > new_row.rfind("."):
            return robot, warehouse  # cannot move
        new_row = "".join(new_row.rsplit(".", 1)) + "."
        warehouse[robot[0]] = [c for c in new_row + row[robot[1] :]]
    else:
        if new_row.find("#") < new_row.find("."):
            return robot, warehouse  # cannot move
        new_row = "." + new_row.replace(".", "", 1)
        warehouse[robot[0]] = [c for c in row[: robot[1] + 1] + new_row]
    return next_pos, warehouse


def move_boxes_vertical(
    warehouse: list[list[str]],
    robot: tuple[int, int],
    next_pos: tuple[int, int],
    direction: tuple[int, int],
):
    obj = get_obj(next_pos, warehouse)
    if obj == "[":
        left_pos = next_pos
        right_pos = next_pos[0], next_pos[1] + 1
    elif obj == "]":
        left_pos = next_pos[0], next_pos[1] - 1
        right_pos = next_pos
    box_left = resolve_boxes(warehouse, left_pos, direction)
    box_right = resolve_boxes(warehouse, right_pos, direction)
    if box_left is False or box_right is False:
        return robot, warehouse
    boxes = []
    for box in box_left:
        if box not in boxes:
            boxes.append(box)
    for box in box_right:
        if box not in boxes:
            boxes.append(box)
    if direction == DO:
        boxes.sort(reverse=True)
        for box in boxes:
            warehouse = move_up_or_down(warehouse, box, 1)
    elif direction == UP:
        boxes.sort()
        for box in boxes:
            warehouse = move_up_or_down(warehouse, box, -1)
    return next_pos, warehouse


def move_boxes(
    warehouse: list[list[str]],
    robot: tuple[int, int],
    next_pos: tuple[int, int],
    direction: tuple[int, int],
):
    # when moving left and right, need to consider only that row
    if direction == LE or direction == RI:
        return move_boxes_horizontal(warehouse, robot, next_pos, direction)
    else:
        return move_boxes_vertical(warehouse, robot, next_pos, direction)


def move_robot(warehouse: list[list[str]], robot: tuple[int, int], move: str):
    direction = get_dir(move)
    next_pos = robot[0] + direction[0], robot[1] + direction[1]
    if is_empty(next_pos, warehouse):
        return next_pos, warehouse
    if is_wall(next_pos, warehouse):
        return robot, warehouse
    if is_box(next_pos, warehouse):
        return move_boxes(warehouse, robot, next_pos, direction)
    return robot, warehouse


def travel(warehouse, robot, moves):
    for move in moves:
        robot, warehouse = move_robot(warehouse, robot, move)
    print("final warehouse:")
    for line in warehouse:
        print("".join(line))
    total = 0
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == "[":
                total += 100 * i + j
    print(total)


tmp_house = puzzle_input[0].split("\n")

robot = ()
for i in range(len(tmp_house)):
    tmp_house[i] = tmp_house[i].replace("#", "##")
    tmp_house[i] = tmp_house[i].replace("O", "[]")
    tmp_house[i] = tmp_house[i].replace(".", "..")
    tmp_house[i] = tmp_house[i].replace("@", "@.")
    if "@" in tmp_house[i]:
        j = tmp_house[i].index("@")
        robot = (i, j)
        tmp_house[i] = tmp_house[i].replace("@", ".")
moves = "".join(puzzle_input[1].split())

warehouse = []
for line in tmp_house:
    warehouse.append([c for c in line])

travel(warehouse, robot, moves)
