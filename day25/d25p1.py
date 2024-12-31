day = "day25"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.split("\n") for line in f.read().split("\n\n")]

locks = list(filter(lambda tmp: tmp[0] == "#####", puzzle_input))
keys = list(filter(lambda tmp: tmp[0] == ".....", puzzle_input))

def fits(key: list[str], lock: list[str]):
    for kr, lr in zip(key, lock):
        for krc, lrc in zip(kr, lr):
            if krc == lrc == "#":
                return False
    return True

total = 0
for key in keys:
    for lock in locks:
        if fits(key, lock): total += 1
print(total)