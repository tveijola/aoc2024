day = "day9"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as file:
    puzzle_input = file.read().strip()

# mem_location, block_len, id_number
files = dict()
free = dict()

is_file = True
pointer = 0
idx = 0
for c in puzzle_input:
    block_len = int(c)
    if is_file:
        files[idx] = (pointer, block_len, idx)
    else:
        free[idx] = (pointer, block_len, None)
        idx += 1
    pointer += block_len
    is_file = not is_file

print(f"start, len filesys={len(files)}")
for i in range(len(files) - 1, 0, -1):
    file = files[i]
    for key, val in free.items():
        if val[0] > file[0]:
            break
        if val[1] >= file[1]: # file fits
            new_file = (val[0], file[1], file[2])
            new_free = (val[0] + file[1], val[1] - file[1], val[2])
            files[i] = new_file
            free[key] = new_free
            break

total = 0
for val in files.values():
    start = val[0]
    block_len = val[1]
    id_num = val[2]
    for i in range(block_len):
        total += (start + i) * id_num
print(total)
