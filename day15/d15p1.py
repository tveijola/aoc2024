import re


day = "day15"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

cannot_move = r"^O+#"  # no empty spaces between here and the wall

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


def is_empty(coord: tuple[int, int], warehouse: list[str]):
    return warehouse[coord[0]][coord[1]] == "."


def is_wall(coord: tuple[int, int], warehouse: list[str]):
    return warehouse[coord[0]][coord[1]] == "#"


def get_slice(coord: tuple[int, int], warehouse: list[str], move: str):
    row_idx = coord[0]
    col_idx = coord[1]
    if move == "^":
        col = []
        for i in range(row_idx):
            col.append(warehouse[i][col_idx])
        return "".join(reversed(col))
    if move == "v":
        col = []
        for i in range(row_idx + 1, len(warehouse)):
            col.append(warehouse[i][col_idx])
        return "".join(col)
    if move == "<":
        return "".join(reversed(warehouse[row_idx][:col_idx]))
    if move == ">":
        return warehouse[row_idx][col_idx + 1 :]


def move_boxes(warehouse: list[str], robot: tuple[int, int], move: str, count: int):
    count = count + 1
    direction = get_dir(move)
    next_pos = robot[0] + direction[0], robot[1] + direction[1]
    last_box_pos = count * direction[0] + robot[0], count * direction[1] + robot[1]
    warehouse[next_pos[0]] = (
        warehouse[next_pos[0]][: next_pos[1]]
        + "."
        + warehouse[next_pos[0]][next_pos[1] + 1 :]
    )
    warehouse[last_box_pos[0]] = (
        warehouse[last_box_pos[0]][: last_box_pos[1]]
        + "O"
        + warehouse[last_box_pos[0]][last_box_pos[1] + 1 :]
    )
    return next_pos, warehouse


def move_robot(warehouse: list[str], robot: tuple[int, int], move: str):
    direction = get_dir(move)
    next_pos = robot[0] + direction[0], robot[1] + direction[1]
    if is_empty(next_pos, warehouse):
        return next_pos, warehouse
    if is_wall(next_pos, warehouse):
        return robot, warehouse
    map_slice = get_slice(robot, warehouse, move)
    if re.search(cannot_move, map_slice) is None:
        # there is one empty space between us and the wall
        boxes = 0
        for char in map_slice:
            if char == "O":
                boxes += 1
            else:
                break
        return move_boxes(warehouse, robot, move, boxes)
    return robot, warehouse


def travel(warehouse, robot, moves):
    for move in moves:
        robot, warehouse = move_robot(warehouse, robot, move)
    print("final warehouse:")
    for line in warehouse:
        print(line)
    total = 0
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == "O":
                total += 100 * i + j
    print(total)


warehouse = puzzle_input[0].split("\n")
moves = "".join(puzzle_input[1].split())


robot = ()
for i in range(len(warehouse)):
    line = warehouse[i]
    if "@" in line:
        j = line.index("@")
        robot = (i, j)
        warehouse[i] = line.replace("@", ".")
        break

travel(warehouse, robot, moves)
