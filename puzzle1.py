with open('input1.txt') as f:
    data = f.read().rstrip()

puzzle = data.split('\n')

calories = []
elf = []
for i, line in enumerate(puzzle):
    if line != '':
        elf.append(int(line))
        if i != len(puzzle) - 1:
            continue
    calories.append(elf)
    elf = []

totals = sorted([sum(x) for x in calories])
print(totals[-1])
tops = totals[-3:]
print(sum(tops))
