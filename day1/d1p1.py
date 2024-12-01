
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

left_list = sorted(left_list)
right_list = sorted(right_list)

# print(left_list)
# print(right_list)

def dist(l, r):
    return abs(l - r)

total = 0
for l, r in zip(left_list, right_list):
    total += dist(l, r)

print(total)
    