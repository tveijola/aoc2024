from functools import cache
import math
import queue


day = "day13"

filename = f"./{day}/sample"
# filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.split("\n") for line in f.read().split("\n\n")]

def press_button(pos, button):
    return (pos[0] + button[0], pos[1] + button[1])

def manh_dist(pos, goal):
    return (goal[0] - pos[0]) + (goal[1] - pos[1])

@cache
def calculate_presses(pos: tuple[int, int], goal: tuple[int, int], a: tuple[int, int], b: tuple[int, int], cost, presses: tuple[int, int]):
    if pos == goal:
        return cost
    if pos[0] > goal[0] or pos[1] > goal[1]:
        return math.inf
    pos_if_b = press_button(pos, b)
    cost_if_b = calculate_presses(pos_if_b, goal, a, b, cost + 1, (presses[0], presses[1] + 1))
    pos_if_a = press_button(pos, a)
    cost_if_a = calculate_presses(pos_if_a, goal, a, b, cost + 3, (presses[0] + 1, presses[1]))
    return min(cost_if_b, cost_if_a)

def a_star(goal, a, b):
    start = (0, 0)
    nodes = queue.PriorityQueue()
    g_score = {}
    g_score[start] = 0
    f_score = {}
    f_score[start] = g_score[start] + manh_dist(start, goal)
    nodes.put((f_score[start], (start, (0, 0))))
    while not nodes.empty():
        cost, node = nodes.get()
        current, presses = node
        if current == goal:
            print(f"found goal {cost}")
            return cost
        if presses[0] > 100 or presses[1] > 100 or current[0] > goal[0] or current[1] > goal[1]:
            continue
        for new_pos, press_cost, press in [(press_button(current, a), 3, (1, 0)), (press_button(current, b), 1, (0, 1))]:
            tentative_g_score = g_score.get(current) + press_cost
            if tentative_g_score < g_score.get(new_pos, math.inf):
                g_score[new_pos] = tentative_g_score
                f_score[new_pos] = tentative_g_score + manh_dist(new_pos, goal)
                # if new_pos not in nodes:
                new_presses = presses[0] + press[0], presses[1] + press[1]
                nodes.put((f_score[new_pos], (new_pos, new_presses)))
    return 0
        

def evaluate(game: list[str]):
    a = game[0].split(":")[1]
    b = game[1].split(":")[1]
    ax = int(a.split(",")[0].split("+")[1])
    ay = int(a.split(",")[1].split("+")[1])
    button_a = (ax, ay)
    bx = int(b.split(",")[0].split("+")[1])
    by = int(b.split(",")[1].split("+")[1])
    button_b = (bx, by)
    g = game[2].split(":")[1].split(", ")
    goalx = int(g[0].split("=")[1])
    goaly = int(g[1].split("=")[1])
    goal = (goalx, goaly)
    # print(ax, ay, bx, by, goalx, goaly)
    # cost = calculate_presses((0, 0), goal, button_a, button_b, 0, (0, 0))
    cost = a_star(goal, button_a, button_b)
    print(cost)
    return cost if math.isfinite(cost) else 0

res = sum(evaluate(game) for game in puzzle_input)
print(res) 