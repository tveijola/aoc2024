day = "day9"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as file:
    puzzle_input = file.read().strip()

# mem_location, block_len, id_number
files = []
free = []

is_file = True
pointer = 0
idx = 0
for c in puzzle_input:
    block_len = int(c)
    if is_file:
        files.append((pointer, block_len, idx))
        idx += 1
    else:
        free.append((pointer, block_len, None))
    pointer += block_len
    is_file = not is_file

print(f"start, len filesys={len(files)}")
for i in range(len(files) - 1, 0, -1):
    file = files[i]
    for j in range(len(free)):
        free_block = free[j]
        if free_block[0] > file[0]:
            break
        if free_block[1] >= file[1]: # file fits
            new_file = (free_block[0], file[1], file[2])
            new_free = (free_block[0] + file[1], free_block[1] - file[1], free_block[2])
            files[i] = new_file
            free[j] = new_free
            break

total = 0
for file in files:
    start = file[0]
    block_len = file[1]
    id_num = file[2]
    for i in range(block_len):
        total += (start + i) * id_num
print(total)
