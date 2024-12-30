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

def find_chain(chain: set[str], pc_links: dict[str, list[str]]):
    sets: list[set[str]] = []
    for pc in chain:
        links = pc_links[pc]
        filtered = set(filter(lambda pc: pc not in chain, links))
        sets.append(filtered)
    common = sets.pop()
    for s in sets:
        common.intersection_update(s)
    if len(common) == 0:
        return chain
    next_chain = set([common.pop()]).union(chain)
    return find_chain(next_chain, pc_links)

longest_chain = tuple()
for k, v in pc_links.items():
    for p in v:
        chain = find_chain(set([k, p]), pc_links)
        sorted_chain = tuple(sorted(chain))
        if len(sorted_chain) > len(longest_chain):
            longest_chain = sorted_chain

print(",".join(longest_chain))
