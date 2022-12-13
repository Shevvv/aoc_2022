with open('input4.txt') as f:
    data = f.read().rstrip()

puzzle = data.split('\n')
pairs = [[set(range(int(y.split('-')[0]), int(y.split('-')[1]) + 1)) for y in x.split(',')] for x in puzzle]

count = 0
for pair in pairs:
    if pair[0].issubset(pair[1]) or pair[1].issubset(pair[0]):
        count += 1

print(count)

count = 0
for pair in pairs:
    if pair[0].intersection(pair[1]):
        count += 1

print(count)
