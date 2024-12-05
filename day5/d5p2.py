from functools import cmp_to_key
from math import floor

day = "day5"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    ordering_rules, page_numbers = f.read().split("\n\n")
rules = [tuple(map(int, rule.split("|"))) for rule in ordering_rules.split("\n")]
updates = [list(map(int, update.split(","))) for update in page_numbers.split("\n")]

def mid(ls: list[int]):
    return ls[floor(len(ls) / 2)]

def is_order(rules, update: list):
    # find only relevant rules
    _rules = filter(lambda rule: rule[0] in update and rule[1] in update, rules)
    for rule in _rules:
        if update.index(rule[1]) < update.index(rule[0]):
            return False
    return True

def to_order(rules: list[tuple[int, int]], update: list[int]):
    _rules = list(filter(lambda rule: rule[0] in update and rule[1] in update, rules))
    def cmp(a, b):
        rule = list(filter(lambda _rule: a in _rule and b in _rule, _rules))[0]
        return -1 if rule[0] == a else 1
    return sorted(update, key=cmp_to_key(cmp))

unordered = filter(lambda update: not is_order(rules, update), updates)
reordered = map(lambda update: to_order(rules, update), unordered)
print(sum([mid(ls) for ls in reordered]))
