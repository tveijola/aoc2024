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
    # filter only relevant rules
    _rules = filter(lambda rule: rule[0] in update and rule[1] in update, rules)
    for rule in _rules:
        if update.index(rule[1]) < update.index(rule[0]):
            return 0
    return mid(update)

print(sum([is_order(rules, update) for update in updates]))
