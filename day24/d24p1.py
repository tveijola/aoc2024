from dataclasses import dataclass
from enum import Enum

day = "day24"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().split("\n\n")

class Oper(Enum):
    AND = 0
    OR = 1
    XOR = 2

    @staticmethod
    def from_str(s: str):
        if s == "AND": return Oper.AND
        if s == "OR": return Oper.OR
        if s == "XOR": return Oper.XOR
        raise RuntimeError(f"incorrect Oper str {s}")

@dataclass
class Gate:
    in1: str
    in2: str
    op: Oper
    out: str

inputs = {
    k: int(v) for k, v in [line.split(": ") for line in puzzle_input[0].split("\n")]
}

gates: list[Gate] = []
for line in puzzle_input[1].split("\n"):
    start, end = line.split(" -> ")
    in1, op, in2 = start.split(" ")
    gates.append(Gate(in1, in2, Oper.from_str(op), end))

def process(in1: int, in2: int, oper: Oper):
    if oper == Oper.AND:
        return in1 and in2
    if oper == Oper.OR:
        return in1 or in2
    if oper == Oper.XOR:
        return in1 ^ in2

while len(gates) > 0:
    gate = gates.pop(0)
    if gate.in1 not in inputs or gate.in2 not in inputs:
        gates.append(gate)
        continue
    # process
    in1 = inputs[gate.in1]
    in2 = inputs[gate.in2]
    result = process(in1, in2, gate.op)
    inputs[gate.out] = result

final_result = ""
z_labels = sorted(filter(lambda l: l.startswith("z"), inputs.keys()))
for label in z_labels:
    final_result += str(inputs[label])
print(int("".join(reversed(final_result)), 2))