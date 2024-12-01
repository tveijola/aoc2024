pi = [int(x) for x in open("./day1/data").read().split()]
print(sum(abs(l - r) for l, r in zip(sorted(pi[::2]), sorted(pi[1::2])))) # part 1
print(sum(l * pi[1::2].count(l) for l in pi[::2])) # part 2