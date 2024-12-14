day = "day14"

# filename = f"./{day}/sample"
# height = 7
# width = 11
filename = f"./{day}/data"
height = 103
width = 101

seconds = 100000

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

def parse_robot(robot: str):
    robot = robot.split()
    pos = tuple(map(int, robot[0].split("=")[1].split(",")))
    vel = tuple(map(int, robot[1].split("=")[1].split(",")))
    return pos, vel

def next_pos(robot):
    pos, vel = robot
    end_pos = (vel[0] + pos[0], vel[1] + pos[1]) 
    end_pos = end_pos[0] % width, end_pos[1] % height
    return end_pos, vel

tl, tr, bl, br = 0, 0, 0, 0
mid_width = int(width / 2)
mid_height = int(height / 2)

def print_layout(positions: list[tuple]):
    layout = []
    for _ in range(height):
        row = ["."] * width
        layout.append(row)
    for pos in positions:
        layout[pos[1]][pos[0]] = "X"
    for line in layout:
        print("".join(line))
    input()

robots = [parse_robot(robot) for robot in puzzle_input]

target = 93
for s in range(1, seconds + 1):
    for i in range(len(robots)):
        robots[i] = next_pos(robots[i])
    positions = [r[0] for r in robots]
    if s == target:
        target += 101
        print(f"seconds: {s}")
        print_layout(positions)