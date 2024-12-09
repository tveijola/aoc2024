day = "day9"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = f.read().strip()

files = []
free_spaces = []
is_file = True
id_number = -1
for c in puzzle_input:
    block_len = int(c)
    if is_file:
        id_number += 1
        files.append((str(id_number), block_len))
    else:
        free_spaces.append(block_len)
    is_file = not is_file

# start with the first file
label, block_len = files.pop(0)
result = [label for _ in range(block_len)]
done = False

print(f"start, len files={len(files)}, len free_space={len(free_spaces)}")
print(f"num of empty files: {len(list(filter(lambda x: x == 0, files)))}")
print(f"num of empty free spaces: {len(list(filter(lambda x: x == 0, free_spaces)))}")

while len(free_spaces) > 0 and len(files) > 0:
    free_space = free_spaces.pop(0) # first empty space
    while free_space > 0:
        label, block_len = files.pop()
        result.append(label)
        block_len -= 1
        if (block_len > 0):
            files.append((label, block_len))
        free_space -= 1
    label, block_len = files.pop(0) # next file
    for _ in range(block_len):
        result.append(label) # push whole file

print(f"done, len files={len(files)}, len free_space={len(free_spaces)}")

total = 0
for i in range(len(result)):
    total += i * int(result[i])
print(total)

#incorrect: 86628406702