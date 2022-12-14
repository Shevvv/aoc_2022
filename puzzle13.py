from functools import total_ordering


@total_ordering
class Packet:

    def __init__(self, inp):
        self.elements = []
        self.parse_input(inp)

    def parse_input(self, inp):
        inp = inp[1:-1]

        i0 = 0
        count = 0
        for i, char in enumerate(inp):
            if char == '[':
                count += 1
            elif char == ']':
                count -= 1

            if i == len(inp) - 1 or (inp[i + 1] == ',' and count == 0):
                section = inp[i0:i + 1]
                try:
                    section = int(section)
                except ValueError:
                    section = Packet(section)
                self.elements.append(section)
                i0 = i + 2

    def __eq__(self, other):
        if len(self.elements) != len(other.elements):
            return False

        evals = []
        for i, element in enumerate(self.elements):
            other_element = other.elements[i]
            element, other_element = self.element_typing(element, other_element)
            evals.append(element == other_element)
        return all(evals)

    def __le__(self, other):
        for i, element in enumerate(self.elements):
            if i == len(other.elements):
                return False
            other_element = other.elements[i]
            element, other_element = self.element_typing(element, other_element)
            if element > other_element:
                return False
            elif element < other_element:
                return True
        return True

    def __str__(self):
        return f'<class.Packet>: [{",".join([str(element) for element in self.elements])}]'

    @staticmethod
    def element_typing(element, other_element):
        if type(element) != type(other_element):
            if isinstance(element, int):
                element = Packet(f"[{element}]")
            else:
                other_element = Packet(f"[{other_element}]")
        return element, other_element


with open('input13.txt') as f:
    data = f.read().rstrip()
puzzle = [x.split('\n') for x in data.split('\n\n')]
pairs = [(Packet(x[0]), Packet(x[1])) for x in puzzle]

correct_order = []
for i, pair in enumerate(pairs):
    if pair[0] <= pair[1]:
        correct_order.append(i + 1)
print(sum(correct_order))

all_packets = [packet for pair in pairs for packet in pair]
dividers = (Packet('[[2]]'), Packet('[[6]]'))
all_packets.extend(dividers)
sorted_packets = sorted(all_packets)
divider_indices = []
for divider in dividers:
    divider_indices.append(sorted_packets.index(divider) + 1)
print(divider_indices[0] * divider_indices[1])
