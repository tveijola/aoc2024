day = "day3"
import re

# filename = f"./{day}/sample"
filename = f"./{day}/data"

mul_regex = r"mul\(\d+,\d+\)"
mul_com = re.compile(mul_regex)

strip_regex = r"don't\(\).+?do\(\)"
strip_com = re.compile(strip_regex, flags=re.S)

with open(filename) as f:
    puzzle_input = strip_com.sub("", f.read())

res: list[str] = mul_com.findall(puzzle_input)
total = 0
for expr in res:
    r, l = expr.lstrip("mul(").rstrip(")").split(",")
    total += int(r) * int(l)

print(total)