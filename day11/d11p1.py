from itertools import chain

day = "day11"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = list(map(int, f.read().strip().split()))

def transform(stone: int):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    digit_count = len(stone_str)
    if (digit_count % 2 == 0):
        mid = int(digit_count / 2)
        return [int(stone_str[:mid]), int(stone_str[mid:])]
    else:
        return [stone * 2024]
 
blinks = 25
stones = puzzle_input
for i in range(blinks):
    stones = list(chain.from_iterable(map(transform, stones)))
print(len(stones))