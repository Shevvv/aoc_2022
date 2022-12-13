class TreeGrid:

    def __init__(self, input_grid):
        self.length = len(input_grid[0])
        self.height = len(input_grid)

        self.grid = []
        for j in range(self.height):
            line = []
            for i in range(self.length):
                line.append(Tree(input_grid[j][i]))
            self.grid.append(line)
        self.check_visibility()
        self.check_distances()

    def check_visibility(self):
        for j0, line in enumerate(self.grid):
            for i0, tree in enumerate(line):
                top = all([True if self.grid[j][i0].height < tree.height else False for j in range(0, j0)])
                right = all([True if self.grid[j0][i].height < tree.height else False for i in range(0, i0)])
                bottom = all([True if self.grid[j][i0].height < tree.height else False
                              for j in range(j0 + 1, self.height)])
                left = all([True if self.grid[j0][i].height < tree.height else False
                            for i in range(i0 + 1, self.length)])

                tree.visible = True if any([top, right, bottom, left]) else False

    def count_visibles(self):
        count = 0
        for line in self.grid:
            for tree in line:
                if tree.visible:
                    count += 1
        return count

    def check_distances(self) -> None:
        def slider(tree: Tree, direction: list) -> int:
            current_height = 0
            count = 0
            i = 0
            while current_height < tree.height and i < len(direction):
                count += 1
                current_height = direction[i].width
                i += 1
            return count

        for j0, line in enumerate(self.grid):
            for i0, tree in enumerate(line):
                top = slider(tree, [self.grid[j][i0] for j in range(j0 - 1, -1, -1)])
                left = slider(tree, [self.grid[j0][i] for i in range(i0 - 1, -1, -1)])
                bottom = slider(tree, [self.grid[j][i0] for j in range(j0 + 1, self.height)])
                right = slider(tree, [self.grid[j0][i] for i in range(i0 + 1, self.length)])
                tree.distance = top * left * bottom * right


class Tree:

    def __init__(self, height):
        self.height = height
        self.visible = None
        self.distance = 0


with open('input8.txt') as f:
    data = f.read().rstrip()
puzzle = [[int(x) for x in line] for line in data.split('\n')]
tree_grid = TreeGrid(puzzle)
print(tree_grid.count_visibles())

distances = [tree.distance for line in tree_grid.grid for tree in line]
print(max(distances))
