class CrateStack:

    def __init__(self, init_state):
        self.stacks = [[x[i] for x in init_state if len(x) > i and x[i]] for i in range(len(init_state[0]))]

    def crane(self, cmd, model=9000):
        words = cmd.split()
        amount = int(words[1])
        start = int(words[3]) - 1
        end = int(words[5]) - 1

        if model == 9000:
            for _ in range(amount):
                self.stacks[end].append(self.stacks[start].pop())

        elif model == 9001:
            grab_index = len(self.stacks[start]) - amount
            picked_up = self.stacks[start][grab_index:]
            del self.stacks[start][grab_index:]
            self.stacks[end].extend(picked_up)

        else:
            raise ValueError(f"{model} is not a valid model of the crane.")

    def check_tops(self):
        return ''.join([x[-1] for x in self.stacks])


with open('input5.txt') as f:
    data = f.read().rstrip()
puzzle = data.split('\n\n')

init_state_raw = puzzle[0].split('\n')[:-1]
init_state = []
for line in init_state_raw:
    level = []
    while len(line) > 2:
        level.append(line[1]) if line[1] != ' ' else level.append(None)
        line = line[4:]
    init_state.append(level)
init_state.reverse()

crate_stack = CrateStack(init_state)
for cmd in puzzle[1].split('\n'):
    crate_stack.crane(cmd)
print(crate_stack.check_tops())

crate_stack = CrateStack(init_state)
for cmd in puzzle[1].split('\n'):
    crate_stack.crane(cmd, 9001)
print(crate_stack.check_tops())
