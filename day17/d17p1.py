day = "day17"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split("\n\n")

regs = puzzle_input[0].split("\n")
reg_a = int(regs[0].split(": ")[1])
reg_b = int(regs[1].split(": ")[1])
reg_c = int(regs[2].split(": ")[1])
prg = list(map(int, puzzle_input[1].split(": ")[1].split(",")))

regs = {
    "a": reg_a,
    "b": reg_b,
    "c": reg_c
}

outs = []

def combo(operand: int):
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return regs["a"]
    if operand == 5:
        return regs["b"]
    if operand == 6:
        return regs["c"]
    else:
        raise RuntimeError(f"unexpected operand for combo: {operand}")

def adv(operand):
    regs["a"] = int(regs["a"] / (2 ** combo(operand)))

def bxl(operand):
    regs["b"] = regs["b"] ^ operand

def bst(operand):
    regs["b"] = combo(operand) % 8

def bxc():
    regs["b"] = regs["b"] ^ regs["c"]

def out(operand):
    outs.append(combo(operand) % 8)

def bdv(operand):
    regs["b"] = int(regs["a"] / (2 ** combo(operand)))

def cdv(operand):
    regs["c"] = int(regs["a"] / (2 ** combo(operand)))

pointer = 0
while True:
    if pointer >= len(prg):
        break
    opcode = prg[pointer]
    operand = prg[pointer + 1]
    if opcode == 0:
        adv(operand)
    if opcode == 1:
        bxl(operand)
    if opcode == 2:
        bst(operand)
    if opcode == 3 and regs["a"] != 0:
        pointer = operand
        continue # skip pointer increment
    if opcode == 4:
        bxc()
    if opcode == 5:
        out(operand)
    if opcode == 6:
        bdv(operand)
    if opcode == 7:
        cdv(operand)
    pointer += 2
print(",".join(map(str, outs)))