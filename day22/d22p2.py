day = "day22"

# filename = f"./{day}/sample"
filename = f"./{day}/data"

with open(filename) as f:
    puzzle_input = list(map(int, f.readlines()))

def mix(secret: int, modified):
    return secret ^ modified

def prune(secret: int):
    return secret % 16777216

def next_number(secret: int):
    num = mix(secret, secret * 64)
    num = prune(num)
    num = mix(num, int(num / 32))
    num = prune(num)
    num = mix(num, num * 2048)
    return prune(num)

def divide_sequence(change_sequence: list[int], secret_sequence: list[int]):
    d = dict()
    for i in range(len(change_sequence) - 3):
        short_seq = tuple(change_sequence[i:i+4])
        price = secret_sequence[i+4]
        if short_seq not in d:
            d[short_seq] = price
    return d

def generate_data(secret_init: int, sequence_length: int):
    secrets = [secret_init % 10]
    secret = secret_init
    changes = []
    for _ in range(sequence_length):
        previous = secret
        secret = next_number(secret)
        secrets.append(secret % 10)
        changes.append(secret % 10 - previous % 10)
    return divide_sequence(changes, secrets)

def analyze_full_data(full_data: list[dict[tuple, int]], unique_short_sequences: set):
    max_bananas = 0
    for ss in unique_short_sequences:
        bananas = 0
        for data_set in full_data:
            if ss in data_set.keys():
                bananas += data_set.get(ss)
        if bananas > max_bananas:
            max_bananas = bananas
            print(f"set {ss} bananas: {bananas}")

sequence_length = 2000
secrets_init = puzzle_input

print("generating full data")
full_data = [generate_data(secret, sequence_length) for secret in secrets_init]
print("full data generated")

short_sequence_counts = dict()
for data_set in full_data:
    for ss in data_set.keys():
        if ss not in short_sequence_counts:
            short_sequence_counts[ss] = 1
        else:
            short_sequence_counts[ss] += 1

unique_short_sequences = set()
for key, val in short_sequence_counts.items():
    if val > 200:
        unique_short_sequences.add(key)
analyze_full_data(full_data, unique_short_sequences)