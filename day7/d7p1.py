from itertools import product


day = "day7"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip() for line in f.readlines()]

PLUS = "+"
MULT = "*"
OPERANDS = [PLUS, MULT]

def evaluate_perm(nums: list[int], perm: tuple[str, ...]):
    val, rest = nums[0], nums[1:]
    for num, oper in zip(rest, perm):
        if (oper == PLUS):
            val += num
        elif (oper == MULT):
            val *= num
    return val

def evaluate(line: str):
    tokens = line.split(":")
    test_val = int(tokens[0])
    nums = [int(x) for x in tokens[1].split()]
    num_oper = len(nums) - 1
    for perm in product(OPERANDS, repeat=num_oper):
        if test_val == evaluate_perm(nums, perm):
            return test_val
    return 0

print(sum(evaluate(line) for line in puzzle_input))
