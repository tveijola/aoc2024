day = "day14"

# filename = f"./{day}/sample"
# height = 7
# width = 11
filename = f"./{day}/data"
height = 103
width = 101

seconds = 10

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

def calculate_end_pos(robot: str, seconds: int):
    robot = robot.split()
    pos = tuple(map(int, robot[0].split("=")[1].split(",")))
    vel = tuple(map(int, robot[1].split("=")[1].split(",")))
    end_pos = (vel[0] * seconds + pos[0], vel[1] * seconds + pos[1]) 
    end_pos = end_pos[0] % width, end_pos[1] % height
    return end_pos

tl, tr, bl, br = 0, 0, 0, 0
mid_width = int(width / 2)
mid_height = int(height / 2)

for s in range(1, seconds + 1):
    for pos in [calculate_end_pos(robot, s) for robot in puzzle_input]:
        if pos[0] > mid_width and pos[1] > mid_height:
            br += 1
        if pos[0] > mid_width and pos[1] < mid_height:
            tr += 1
        if pos[0] < mid_width and pos[1] > mid_height:
            bl += 1
        if pos[0] < mid_width and pos[1] < mid_height:
            tl += 1
    print(f"{br}, {tr}, {bl}, {tl}")
    break
