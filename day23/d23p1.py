day = "day23"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = [line.strip().split("-") for line in f.readlines()]

pc_links: dict[str, list[str]] = dict()
for pc_pair in puzzle_input:
    f, s = pc_pair
    if f in pc_links:
        pc_links[f] += [s]
    else:
        pc_links[f] = [s]
    if s in pc_links:
        pc_links[s] += [f]
    else:
        pc_links[s] = [f]

inter_connected: set[tuple[str]] = set()
for pc, linked_pcs in pc_links.items():
    for linked_pc in linked_pcs:
        next_links = pc_links[linked_pc]
        for tmp in next_links:
            if tmp in linked_pcs:
                pc_set = [pc, linked_pc, tmp]
                inter_connected.add(tuple(sorted(pc_set)))

filtered = set(filter(lambda x: any([pc.startswith("t") for pc in x]), inter_connected))
print(len(filtered))