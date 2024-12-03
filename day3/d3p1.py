day = "day3"
import re

# filename = f"./{day}/sample"
filename = f"./{day}/data"

regex_str = r"mul\(\d+,\d+\)"
regex_com = re.compile(regex_str)

with open(filename) as f:
    puzzle_input = f.read()

res: list[str] = regex_com.findall(puzzle_input)
total = 0
for expr in res:
    r, l = expr.lstrip("mul(").rstrip(")").split(",")
    total += int(r) * int(l)

print(total)