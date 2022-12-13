from string import ascii_lowercase, ascii_uppercase

types = ascii_lowercase + ascii_uppercase

with open('input3.txt') as f:
    data = f.read().rstrip()

puzzle = data.split('\n')
sacks = [[set(sack[:int(len(sack)/2)]), set(sack[int(len(sack)/2):])] for sack in puzzle]

overall_shared = []
for sack in sacks:
    shared = sack[0].intersection(sack[1])
    overall_shared.extend(shared)

score = 0
for shared in overall_shared:
    score += types.index(shared) + 1

print(score)

score = 0
for i in range(len(sacks)):
    if i % 3 == 2:
        sack_1 = sacks[i - 2][0].union(sacks[i - 2][1])
        sack_2 = sacks[i - 1][0].union(sacks[i - 1][1])
        sack_3 = sacks[i][0].union(sacks[i][1])

        badge = sack_1.intersection(sack_2).intersection(sack_3)
        if len(badge) != 1:
            raise RuntimeError(f"there's more than 1 badge at line {i}.")
        score += types.index(badge.pop()) + 1

print(score)

