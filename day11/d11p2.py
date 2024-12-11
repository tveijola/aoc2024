from functools import cache

day = "day11"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = list(map(int, f.read().strip().split()))

@cache
def calculate_stones(stone: int, blinks: int):
    if blinks == 0:
        return 1
    if stone == 0:
        return calculate_stones(1, blinks - 1)  
    stone_str = str(stone)
    digit_count = len(stone_str)
    if (digit_count % 2 == 0):
        mid = int(digit_count / 2)
        return calculate_stones(int(stone_str[:mid]), blinks - 1) + calculate_stones(int(stone_str[mid:]), blinks - 1)
    return calculate_stones(stone * 2024, blinks - 1)

blinks = 75
final = sum(calculate_stones(stone, blinks) for stone in puzzle_input)
print(final)