def manhattan(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def find_manhattan_x(point, y, d):
    x1 = abs(point[1] - y) + point[0] - d
    x2 = d - abs(point[1] - y) + point[0]
    if x1 < x2:
        return x1, x2


def compare_ranges(range1, range2):
    if range1[0] < range2[0] <= range1[1] <= range2[1]:
        return 'overlaps right'
    if range2[0] <= range1[0] <= range2[1] < range1[1]:
        return 'overlaps left'
    if range2[0] <= range1[0] <= range1[1] <= range2[1]:
        return 'inside'
    if range1[0] <= range2[0] <= range2[1] <= range1[1]:
        return 'contains'
    return 'outside'


def collapse_ranges(input_ranges):
    output_ranges = []
    sorted_input_ranges = sorted(input_ranges, key=lambda x: x[0])
    for input_range in sorted_input_ranges:
        if not output_ranges:
            output_ranges.append(input_range)

        processed = False
        for i, output_range in enumerate(output_ranges):
            match compare_ranges(input_range, output_range):
                case 'overlaps left':
                    output_ranges[i] = (output_range[0], input_range[1])
                    processed = True
                    break
                case 'inside':
                    processed = True
                    break
                case 'contains':
                    output_ranges[i] = input_range
                    processed = True
                    break
                case 'outside':
                    processed = False
                    continue
        if not processed:
            output_ranges.append(input_range)

    return output_ranges


def compute_fill_ranges(puzzle, y):
    fill_ranges = []
    for line in puzzle:
        fill_range = find_manhattan_x(line[0], y, line[2])
        if fill_range:
            fill_ranges.append(fill_range)
    return fill_ranges


def project_ranges_onto_line(true_ranges, x0=None, xn=None):
    x0 = x0 if x0 is not None else true_ranges[0][0]
    xn = xn if xn is not None else true_ranges[-1][1]
    line_y = [True for _ in range(x0, xn + 1)]
    for true_range in true_ranges:
        if compare_ranges(true_range, (x0, xn)) == 'outside':
            continue
        tr_x0 = true_range[0] if true_range[0] >= x0 else x0
        tr_xn = true_range[1] if true_range[1] <= xn else xn
        for i in range(tr_x0, tr_xn + 1):
            line_y[i - x0] = False
    return line_y, x0


def place_beacons(puzzle, line_y, x0, value=True):
    for i in range(len(line_y)):
        for line in puzzle:
            if line[1][1] == y and line[1][0] == i + x0:
                line_y[i] = value


with open('input15.txt') as f:
    data = f.read().rstrip()
s_cue, b_cue = 'Sensor at ', 'closest beacon is at '
puzzle = [[tuple([int(coord.strip('x=').strip('y='))
                 for coord in obj.removeprefix(s_cue).
                 removeprefix(b_cue).split(', ')])
           for obj in line.split(': ')]
          for line in data.split('\n')]

x_s = [obj[0] for line in puzzle for obj in line]
x0, xn = min(x_s), max(x_s)

for line in puzzle:
    line.append(manhattan(line[0], line[1]))

y = 2_000_000
fill_ranges = compute_fill_ranges(puzzle, y)
true_ranges = collapse_ranges(fill_ranges)
line_y, x0 = project_ranges_onto_line(true_ranges)
place_beacons(puzzle, line_y, x0, True)
print(line_y.count(False))

x0, xn = 0, 4_000_000
for y in range(4_000_001):
    if y % 100000 == 0:
        print('{:,}'.format(y).replace(',', ' '), '/ 4 000 000')

    fill_ranges = compute_fill_ranges(puzzle, y)
    true_ranges = collapse_ranges(fill_ranges)
    if len(true_ranges) > 1:
        print((true_ranges[0][-1] + 1) * 4_000_000 + y)
        break
