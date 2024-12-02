day = "day2"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split("\n")

reports = []
for report in puzzle_input:
    reports.append([int(x) for x in report.split()])

def levels_safe(level1: int, level2: int):
    return level2 > level1 and abs(level1 - level2) <= 3

def asc(report: list[int]):
    return all([levels_safe(report[i-1], report[i]) for i in range(1, len(report))]) 

def desc(report: list[int]):
    return asc(list(reversed(report)))

def safe(report: list[int], ridx=-1):
    if ridx >= len(report):
        return False
    if ridx >= 0:
        mod_report = list(report)
        mod_report.pop(ridx)
        return asc(mod_report) or desc(mod_report) or safe(report, ridx+1)
    else:
        return asc(report) or desc(report) or safe(report, ridx+1)

total_safe = 0
for report in reports:
    total_safe += int(safe(report))

print(total_safe)