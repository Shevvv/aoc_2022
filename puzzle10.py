from string import digits


digit_set = set(digits)
digit_set.add('-')


def full_report(func):
    reports = []

    def wrapper(self, i, end):
        report = func(self, i, end)
        if report:
            reports.append(report)
        if i == end - 1:
            print(sum(reports))
    return wrapper


class Circuit:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = [[' ' for _ in range(40)] for _ in range(6)]

        self.cycle = 0
        self.x = 1
        self.target_x = None
        self.target_cycle = None
        self.COMMANDS = {
            'noop': self.noop,
            'addx': self.addx,
        }

    def light_pixel(self):
        if self.x - 1 <= self.cycle % self.width <= self.x + 1:
            self.image[self.cycle // self.width][self.cycle % self.width] = '\u2588'

    def add_cycle(self):
        self.light_pixel()
        self.cycle += 1
        if self.cycle == self.target_cycle:
            self.x = self.target_x
            return True
        return False

    def noop(self):
        self.target_x = self.x
        self.target_cycle = self.cycle + 1

    def addx(self, v):
        self.target_x = self.x + v
        self.target_cycle = self.cycle + 2

    def comm_hub(self, *args):
        comm = self.COMMANDS[args[0]]
        comm(*args[1:])

    def execute_commands(self, comm_list, report=False):
        read_command = True

        for i in range(self.width * self.height):
            if read_command and comm_list:
                self.comm_hub(*comm_list.pop(0))
            if report:
                self.report(i, self.width * self.height)
            read_command = self.add_cycle()

    @full_report
    def report(self, i, steps):
        if i % self.width == self.width // 2 - 1:
            print(f"{i + 1}: x: {self.x}, signal strength: {self.x * (i + 1)}")
            return self.x * (i + 1)

    def __str__(self):
        return "\n".join([''.join(x) for x in self.image])


with open('input10.txt') as f:
    data = f.read().rstrip()
puzzle = [[int(x) if set(x).issubset(digit_set) else x for x in line.split()] for line in data.split('\n')]

circuit = Circuit(40, 6)
circuit.execute_commands(puzzle, True)
print(circuit)
