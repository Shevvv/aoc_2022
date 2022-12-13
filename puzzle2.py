shapes = {
    'rock': {
        'op': 'A',
        'pl': 'X',
        'score': 1,
        'beats': 'scissors',
    },
    'paper': {
        'op': 'B',
        'pl': 'Y',
        'score': 2,
        'beats': 'rock',
    },
    'scissors': {
        'op': 'C',
        'pl': 'Z',
        'score': 3,
        'beats': 'paper',
    },
}

pl_shapes_lookup = {shapes[x]['pl']: x for x in shapes.keys()}
op_shapes_lookup = {shapes[x]['op']: x for x in shapes.keys()}
wins_lookup = {shapes[x]['beats']: x for x in shapes.keys()}

with open('input2.txt') as f:
    data = f.read().rstrip()

puzzle = [x.split() for x in data.split('\n')]

score = 0
for rps_round in puzzle:
    op_shape = op_shapes_lookup[rps_round[0]]
    pl_shape = pl_shapes_lookup[rps_round[1]]

    score += shapes[pl_shape]['score']
    if pl_shape == op_shape:
        score += 3
    elif shapes[pl_shape]['beats'] == op_shape:
        score += 6

print(score)

score = 0
for rps_round in puzzle:
    op_shape = op_shapes_lookup[rps_round[0]]
    if rps_round[1] == 'X':
        score += shapes[shapes[op_shape]['beats']]['score']
    elif rps_round[1] == 'Y':
        score += 3 + shapes[op_shape]['score']
    else:
        score += 6 + shapes[wins_lookup[op_shape]]['score']

print(score)
