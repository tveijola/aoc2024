from functools import cache

day = "day1"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

left_list = []
right_list = []
for line in puzzle_input:
    left, right = line.split("   ")
    left_list.append(int(left))
    right_list.append(int(right))

right_list = tuple(right_list)

@cache
def similarity(num: int, r: list[int]):
    count = r.count(num)
    return num * count

total = 0
for l in left_list:
    total += similarity(l, right_list)

print(total)