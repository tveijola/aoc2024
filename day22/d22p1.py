

day = "day22"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = list(map(int, f.readlines()))

print(puzzle_input)

def mix(secret: int, modified):
    return secret ^ modified

def prune(secret: int):
    return secret % 16777216

def next_number(secret: int):
    num = mix(secret, secret * 64)
    num = prune(num)
    num = mix(num, int(num / 32))
    num = prune(num)
    num = mix(num, num * 2048)
    return prune(num)

total = 0
for secret in puzzle_input:
    for _ in range(2000):
        secret = next_number(secret)
    total += secret
print(total)