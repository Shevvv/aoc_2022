class Element:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


class Directory(Element):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.contents = []

    def add_file(self, name, parent, size):
        self.contents.append(File(name, parent, size))

    def add_dir(self, name, parent):
        self.contents.append(Directory(name, parent))

    def switch_dir(self, name):
        for element in self.contents:
            if isinstance(element, Directory) and element.name == name:
                return element

    def get_size(self):
        size = 0
        for element in self.contents:
            if isinstance(element, File):
                size += element.size
            elif isinstance(element, Directory):
                size += element.get_size()
            else:
                raise RuntimeError(f'directory {self.name} contains unsupported type {type(element)}.')

        return size

    def get_every_child(self):
        childs = []
        for element in self.contents:
            if isinstance(element, Directory):
                childs.append(element)
                childs.extend(element.get_every_child())
        return childs


class File(Element):

    def __init__(self, name, parent, size):
        super().__init__(name, parent)
        self.size = size


def cd_com(new_dir):
    global current_dir
    global root
    if new_dir == '/':
        current_dir = root
    elif new_dir == '..':
        current_dir = current_dir.parent
    else:
        current_dir = current_dir.switch_dir(new_dir)


def ls_com():
    global current_state
    current_state = add_element


def add_element(line):
    global current_dir
    if line[0] != 'dir':
        current_dir.add_file(line[1], current_dir, int(line[0]))
    else:
        current_dir.add_dir(line[1], current_dir)


COMMANDS = {
    'cd': cd_com,
    'ls': ls_com,
}

TOTAL_SPACE = 70000000
UPDATE_SPACE = 30000000


with open('input7.txt') as f:
    data = f.read().rstrip()
puzzle = [x.split() for x in data.split('\n')]

root = Directory('root', None)
current_dir = root
current_state = None
for line in puzzle:
    if line[0] == '$':
        COMMANDS[line[1]](*line[2:])
    else:
        current_state(line)

directories = root.get_every_child()
size_count = 0
for directory in directories:
    if directory.get_size() <= 100000:
        size_count += directory.get_size()
print(size_count)

unused_space = TOTAL_SPACE - root.get_size()
required_space = UPDATE_SPACE - unused_space
candidates = []
candidate_spaces = []
for directory in directories:
    if directory.get_size() >= required_space:
        candidates.append(directory)
        candidate_spaces.append(directory.get_size())

print(min(candidate_spaces))
