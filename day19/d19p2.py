from dataclasses import dataclass
from enum import IntEnum, unique
from functools import cache


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

@dataclass(frozen=True)
class Towel:
    pattern: tuple[Stripe]

tmp = puzzle_input[0].split(", ")
available_towels = []
for pattern in tmp:
    towel_pattern = tuple(STRIPES[c] for c in pattern)
    available_towels.append(Towel(towel_pattern))
available_towels = tuple(towel for towel in available_towels)

tmp = puzzle_input[1].split("\n")
desired_patterns: list[tuple[Stripe]] = []
for pattern in tmp:
    towel_pattern = tuple(STRIPES[c] for c in pattern)
    desired_patterns.append(towel_pattern)

@cache
def create_pattern(available: tuple[Towel], desired: tuple[Stripe]):
    if len(desired) == 0:
        return 1
    possibles: list[Towel] = []
    for towel in available:
        if towel.pattern == desired[:len(towel.pattern)]:
            possibles.append(towel)
    if len(possibles) == 0:
        return 0
    total = 0
    for possible in possibles:
        covered = len(possible.pattern)
        total += create_pattern(available, desired[covered:])
    return total

possibles = 0
for pattern in desired_patterns:
    possible = create_pattern(available_towels, pattern)
    possibles += possible
print(possibles)
