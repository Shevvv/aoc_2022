import numpy as np


class Sand:

    def __init__(self, cave):
        self.cave = cave
        self.start = (500 - self.cave.x_0, 0)
        self.grains = []

    def add_grain(self):
        coords = self.start
        j = 0
        while j < self.cave.grid.shape[0]:
            # If the starting point is taken up, return `False`
            if j == 0 and self.cave.grid[j][coords[0]]:
                return False
            # Locate the cell below is taken up, relocate to the cell right
            # above it
            if self.cave.grid[j][coords[0]]:
                coords = (coords[0], j - 1)
            # if we've reached the bottom, return `False`
            elif j == len(self.cave.grid) - 1:
                return False
            # Check next line
            else:
                j += 1
                continue

            # If we're at the edge, add a column. Adding to the left messes
            # up indexing, so correct that, too
            if coords[0] == 0:
                self.cave.add_columns('left', 1)

                coords = (coords[0] + 1, coords[1])
                self.start = (self.start[0] + 1, self.start[0])

                for i, grain in enumerate(self.grains):
                    self.grains[i] = grain[0] + 1, grain[1]
            elif coords[0] == self.cave.grid.shape[1] - 1:
                self.cave.add_columns('right', 1)

            # Determine whether there's place to fall. If not, be at rest
            if not self.cave.grid[j][coords[0] - 1]:
                coords = (coords[0] - 1, j)
            elif not self.cave.grid[j][coords[0] + 1]:
                coords = (coords[0] + 1, j)
            else:
                self.cave.grid[coords[1]][coords[0]] = True
                self.grains.append(coords)
                return True


class Cave:

    def __init__(self, inp):
        self.grid = np.array([])
        self.x_0 = 0
        self.floor = False
        self.parse_inp(inp)

    def parse_inp(self, inp):
        rock_points = [[tuple([int(x) for x in point.split(',')])
                       for point in rock.split(' -> ')]
                       for rock in inp.split('\n')]

        x_s = [point[0] for rock in rock_points for point in rock]
        y_s = [point[1] for rock in rock_points for point in rock]
        self.x_0, x_n = min(x_s) - 1, max(x_s) + 2
        y_n = max(y_s) + 1
        self.grid = np.array([[False for _ in range(self.x_0, x_n)]
                             for _ in range(y_n)])
        norm_points = [[(point[0] - self.x_0, point[1])
                       for point in rock]
                       for rock in rock_points]

        for rock in norm_points:
            starting_point = None
            for point in rock:
                if starting_point:
                    fillers = [(i, j) for i
                               in inclusive_range(starting_point[0], point[0])
                               for j
                               in inclusive_range(starting_point[1], point[1])]
                    for i, j in fillers:
                        self.grid[j][i] = True
                starting_point = point

    def add_floor(self):
        level1 = [False for _ in range(self.grid.shape[1])]
        level0 = [True for _ in range(self.grid.shape[1])]
        self.grid = np.insert(self.grid, self.grid.shape[0], [level1,
                                                             level0], 0)
        self.floor = True

    def add_columns(self, edge, count):
        column = [False for _ in range(self.grid.shape[0])]
        if self.floor:
            column[-1] = True
        columns = [column for _ in range(count)]

        if edge == 'left':
            index = 0
        elif edge == 'right':
            index = self.grid.shape[1]
        else:
            raise ValueError(f'edge value {edge} of method '
                             f'`Cave.add_columns()` not recognized!')

        self.grid = np.insert(self.grid, index, columns, 1)

    def __str__(self):
        return '\n'.join([''.join(['#' if cell else '.'
                                   for cell in line])
                          for line in self.grid])


def inclusive_range(start, end):
    if start <= end:
        return range(start, end + 1)
    return range(end, start + 1)


def visualize_problem(cave, sand, problem):
    cave_str = str(cave)
    lines = cave_str.split('\n')
    last = sand.grains[-1]
    lines[last[1]] = lines[last[1]][:last[0]] + \
                     'O' + lines[last[1]][last[0] + 1:]
    lines[problem[1]] = lines[problem[1]][:problem[0]] + \
                        'X' + lines[problem[1]][problem[0] + 1:]
    print('\n'.join(lines))


with open('input14.txt') as f:
    data = f.read().rstrip()

cave = Cave(data)
sand = Sand(cave)

while sand.add_grain():
    pass
print(len(sand.grains))

cave = Cave(data)
cave.add_floor()
sand = Sand(cave)
while sand.add_grain():
    pass
print(len(sand.grains))
