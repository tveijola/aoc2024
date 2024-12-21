from dataclasses import dataclass
from enum import IntEnum, unique


day = "day19"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split("\n\n")

@unique
class Stripe(IntEnum):
    WHITE = 0,
    BLUE = 1,
    BLACK = 2,
    RED = 3,
    GREEN = 4
    def __repr__(self):
        return self.name

STRIPES: dict[str, Stripe] = {
    "w": Stripe.WHITE,
    "u": Stripe.BLUE,
    "b": Stripe.BLACK,
    "r": Stripe.RED,
    "g": Stripe.GREEN,
}

@dataclass
class Towel:
    pattern: list[Stripe]

tmp = puzzle_input[0].split(", ")
available_towels: list[Towel] = []
for pattern in tmp:
    towel_pattern = [STRIPES[c] for c in pattern]
    available_towels.append(Towel(towel_pattern))

tmp = puzzle_input[1].split("\n")
desired_patterns: list[list[Stripe]] = []
for pattern in tmp:
    towel_pattern = [STRIPES[c] for c in pattern]
    desired_patterns.append(towel_pattern)

def create_pattern(available: list[Towel], desired: list[Stripe]):
    if len(desired) == 0:
        return 1
    possibles: list[Towel] = []
    for towel in available:
        if towel.pattern == desired[:len(towel.pattern)]:
            possibles.append(towel)
    if len(possibles) == 0:
        return 0
    for possible in possibles:
        covered = len(possible.pattern)
        if create_pattern(available, desired[covered:]) == 1:
            return 1
    return 0

possibles = 0
for pattern in desired_patterns:
    possible = create_pattern(available_towels, pattern)
    possibles += possible
print(possibles)