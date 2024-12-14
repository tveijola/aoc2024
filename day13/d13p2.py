day = "day13"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.split("\n") for line in f.read().split("\n\n")]

def solve_pair(ax, bx, ay, by, goalx, goaly):
    # Solve equation pair
    # ax * A + bx * B = goalx
    # ay * A + by * B = goaly
    bxs = bx * ay
    bys = by * ax
    goalxs = goalx * ay
    goalys = goaly * ax
    bi = bxs - bys
    G = goalxs - goalys
    B = G / bi
    A = (goalx - bx * B) / ax
    return (A, B) if int(A) == A and int(B) == B else (0, 0)
        

def evaluate(game: list[str]):
    a = game[0].split(":")[1]
    b = game[1].split(":")[1]
    ax = int(a.split(",")[0].split("+")[1])
    ay = int(a.split(",")[1].split("+")[1])
    bx = int(b.split(",")[0].split("+")[1])
    by = int(b.split(",")[1].split("+")[1])
    g = game[2].split(":")[1].split(", ")
    goalx = int(g[0].split("=")[1]) + 10000000000000
    goaly = int(g[1].split("=")[1]) + 10000000000000
    A, B = solve_pair(ax, bx, ay, by, goalx, goaly)
    return A * 3 + B

res = sum(evaluate(game) for game in puzzle_input)
print(res) 