from string import ascii_lowercase


class HeightMap:

    def __init__(self, inp):
        self.letter_grid = [[x for x in line] for line in inp.split('\n')]
        self.grid = [[0 if x == 'S' else 25 if x == 'E' else ascii_lowercase.index(x) for x in line]
                     for line in self.letter_grid]
        self.length = len(self.grid[0])
        self.width = len(self.grid)
        self._current_i = 0

    def __str__(self):
        return '\n'.join([''.join([f'{x : 3}' for x in line]) for line in self.grid])

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_i < self.width:
            line = self.grid[self._current_i]
        else:
            raise StopIteration
        self._current_i += 1
        return line

    def __getitem__(self, item):
        return self.grid[item]


class PathCollector:

    NEIGHBORS = (
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    )

    def __init__(self, height_map):
        self.height_map = height_map
        self.grid = None
        self.processing = []
        self.dijkstra()

    def locate_indices_of_cells(self, value, grid=None):
        indices = []
        if not grid:
            grid = self.grid
        for j, line in enumerate(grid):
            for i, cell in enumerate(line):
                if cell == value:
                    indices.append((i, j))
        if not indices:
            raise ValueError(f'requested point {value} could not be located!')
        return indices

    def dijkstra(self, start=None, reverse=False):
        if not start:
            self.build_start(start)
        else:
            self.build_start(start)

        while self.processing:
            current_path_cell = self.pick_path_cell()

            neighbor_indices = self.locate_neighbor_indices(current_path_cell, reverse)
            for neighbor_index in neighbor_indices:
                neighbor = self.grid[neighbor_index[1]][neighbor_index[0]]
                if not neighbor:
                    neighbor = PathCell(current_path_cell)
                    self.grid[neighbor_index[1]][neighbor_index[0]] = neighbor
                    self.processing.append(neighbor)
                elif neighbor not in self.processing:
                    continue

                if bool(neighbor.distance) <= (current_path_cell.distance + 1 < bool(neighbor.distance)):
                    neighbor.distance = current_path_cell.distance + 1

    def build_start(self, start):
        if not start:
            start_coords = self.locate_indices_of_cells('S', self.height_map.letter_grid)[0]
        elif isinstance(start, str):
            start_coords = self.locate_indices_of_cells(start, self.height_map.letter_grid)[0]

        self.grid = [[None for _ in range(height_map.length)] for _ in range(height_map.width)]
        start_path_cell = PathCell(None)
        start_path_cell.distance = 0
        self.processing = []
        self.processing.append(start_path_cell)
        self.grid[start_coords[1]][start_coords[0]] = start_path_cell

    def pick_path_cell(self):
        distances = [path_cell.distance for path_cell in self.processing]
        min_distance = min(distances)
        current_path_cell = self.processing[distances.index(min_distance)]
        del self.processing[self.processing.index(current_path_cell)]
        return current_path_cell

    def locate_neighbor_indices(self, path_cell, reverse):
        path_cell_index = self.locate_indices_of_cells(path_cell)[0]
        abs_neighbor_indices = []

        for neighbor_index in PathCollector.NEIGHBORS:
            i = path_cell_index[0] + neighbor_index[0]
            j = path_cell_index[1] + neighbor_index[1]

            if not (0 <= i < self.height_map.length and 0 <= j < self.height_map.width):
                continue

            if not reverse:
                step_condition = self.height_map[path_cell_index[1]][path_cell_index[0]] + 1 >= self.height_map[j][i]
            else:
                step_condition = self.height_map[path_cell_index[1]][path_cell_index[0]] - 1 <= self.height_map[j][i]
            if step_condition:
                abs_neighbor_indices.append((i, j))
        return abs_neighbor_indices

    def shortest_distance(self, value=None):
        if not value:
            indices = self.locate_indices_of_cells(value='E', grid=self.height_map.letter_grid)[0]
            output = self.grid[indices[1]][indices[0]].distance
        elif isinstance(value, str):
            indices_set = self.locate_indices_of_cells(value, self.height_map.letter_grid)
            output = min([self.grid[ind[1]][ind[0]].distance for ind in indices_set if self.grid[ind[1]][ind[0]]])
        return output

    def show_path(self, cell_index):
        cell = self.grid[cell_index[1]][cell_index[0]]
        index = self.locate_indices_of_cells(cell)[0]
        if cell.entrance:
            entrance_index = self.locate_indices_of_cells(cell.entrance)[0]
            path = self.show_path(entrance_index)
            path.append(index)
        else:
            path = [index]
        return path


class PathCell:

    def __init__(self, entrance):
        self.entrance = entrance
        self.distance = None


with open('input12.txt') as f:
    data = f.read().rstrip()

height_map = HeightMap(data)
path_collector = PathCollector(height_map)
print(path_collector.shortest_distance())
path_collector.dijkstra('E', reverse=True)
print(path_collector.shortest_distance('a'))
