from collections import deque
from math import prod
from copy import deepcopy


class Monkey:
    """
    This class describes a monkey and its items, the operation it performs, the divisor for the test and potential
    monkeys for the items down the line. Employs class methods for performing operations on a collection of monkeys.

    NB: after all monkeys have been created, the class needs to be activated to play rounds! (`Monkey.activate()`)

    Attributes:
        cls.monkeys : `list` of `Monkey` objects
            a collection of every `Monkey` object
        cls.init_monkeys : `list` of `Monkey` objects
            a snapshot of `Monkey.monkeys` after activation
        cls.divisors : `set` of `int`
            all divisors used by monkeys
        cls.activated : `bool`
            tracks whether the class has been activated after the initialization of the last monkey.

        items : `deque` of `int`
            worry levels of every item held by the monkey. Used in relaxed rounds
        remainders_of_items : `deque` of `dict`
            remainders of each worry level in respect to divisors from every monkey in the group
        divisor : `int`
            the test divisor of this specific monkey
        true_monkey : `int`
            the monkey to receive the item should it pass the test
        false_monkey : `int`
            the monkey to receive the item should it fail the test
        count : `int`
            the number of items ever inspected by the monkey

    Methods:
        cls.play_round(relaxed=True) : `None`
            play a single round of the game. Relaxed by default (worry levels are divided by 3 and rounded down after
            applying the operation)
        cls.items_inspected() : `int`
            Retrieve the number of items inspected by every monkey.
        cls.reset() : `None`
            Reset the class to its initial state (same as after activation).
        cls.activate() : `None`
            Activate the class after the last monkey has been initialized. Necessary before playing rounds.

        inspect_item(heap) : same as the elements of `heap`
            Inspect an item, changing its worry level
        take_turn(relaxed) : `None`
            Take a turn, that is, inspect an item, test the worry level and pass the item to the next monkey
        parse_operation(operation) : `Function`
            build a function corresponding to the `str` representation of an operation
        operation(args) : same as the first element of `args`
            perform this specific monkey's operation on the elements of `args`
    """

    monkeys = []
    init_monkeys = []
    divisors = set()
    activated = False

    @classmethod
    def play_round(cls, relaxed=True):
        """
        Play one round of the game. Can only be used with an activated `Monkey` class
        (*i.e.*, no more monkey additions are expected)
        :param relaxed: `bool`, relaxed mode performs division by 3 and floor rounding before testing the item
        :return: `None`
        """
        if not cls.activated:
            raise ValueError('class `Monkey` needs to be activated after initialization of the final monkey!\n'
                             'Use `Monkey.activate()` before playing rounds!')
        for monkey in cls.monkeys:
            monkey.take_turn(relaxed)

    @classmethod
    def items_inspected(cls):
        """
        Retrieve the number of items inspected by every monkey.
        :return: `list` of `int`
        """
        return [monkey.count for monkey in cls.monkeys]

    @classmethod
    def reset(cls):
        """
        Reset the class to its initial state (same as after activation).
        :return: `None`
        """
        cls.monkeys = deepcopy(cls.init_monkeys)

    @classmethod
    def activate(cls):
        """
        Activate the class after the last monkey has been initialized. Necessary before playing rounds.

        This method exists to ensure that items of any monkey are modulo'ed by every monkey's divisor. It also takes
        a snapshot of `cls.monkeys`, necessary for `cls.reset()`.

        :return: `None`
        """
        for i, monkey in enumerate(cls.monkeys):
            for item in monkey.items:
                monkey.remainders_of_items.append({divisor: item % divisor for divisor in cls.divisors})
            cls.init_monkeys.append(deepcopy(monkey))
        cls.activated = True

    def __init__(self, items, operation, divisor, true, false):
        """
        Construct a `Monkey` object.
        :param items: `lst` of `int` or `str`, a list of worry levels of each item held by the monkey
        :param operation: `str` expression (not statement) of the operation performed by the monkey
        :param divisor: `str` or `int` number to test each worry level (if the level is divisable by that number,
            return True)
        :param true: `str` or `int` index of the monkey to receive the item should the worry level succeed the test
        :param false: `str` or `int` index of the monkey to receive the item otherwise
        """
        self.items = deque([int(x) for x in items.split(', ')])
        self.remainders_of_items = deque()

        self.operation = self.parse_operation(operation)

        self.divisor = int(divisor)
        Monkey.divisors.add(self.divisor)

        self.true_monkey = int(true)
        self.false_monkey = int(false)
        self.count = 0
        Monkey.monkeys.append(self)

    def inspect_item(self, heap):
        """
        Inspect the first item in queue `heap` and adjust its worrying level. Increment the number of items
        inspected by this monkey.
        :param heap: a `deque` list of items (`int` or `dict`) to inspect
        :return: same as the elements of `heap`
        """
        item = heap.popleft()
        item = self.operation(item)
        if isinstance(item, int):
            item = item // 3
            # This block is executed in the `relaxed` mode of the game

        self.count += 1
        return item

    def take_turn(self, relaxed):
        """
        Inspect each item in order adjusting their worry level at the same time, assess them and pass to the next monkey
        :param relaxed: `bool`, corresponds to the relaxed mode of the game
        :return: `None`
        """
        # The heap is a `deque` of `int` in the relaxed mode and a `deque` of `dict` otherwise
        heap = self.remainders_of_items
        if relaxed:
            heap = self.items

        while heap:
            item = self.inspect_item(heap)

            # Since two different attributes are used for different modes of the game,
            # 4 cases are described rather than 2
            if relaxed and item % self.divisor == 0:
                Monkey.monkeys[self.true_monkey].items.append(item)
            elif relaxed:
                Monkey.monkeys[self.false_monkey].items.append(item)
            elif not relaxed and item[self.divisor] == 0:
                Monkey.monkeys[self.true_monkey].remainders_of_items.append(item)
            else:
                Monkey.monkeys[self.false_monkey].remainders_of_items.append(item)

    def parse_operation(self, operation):
        """
        Construct the operation performed by the monkey using the `str` input. Since the input is an expression,
        it does not include an assignment operator ("=")
        :param operation: `str`
        :return: `Function`
        """
        FUNCS = {
            '+': add,
            '*': multiply,
        }
        inp = operation.split()     # Generate a `list` with three elements, where the middle one is the operator
        func = FUNCS[inp.pop(1)]

        def wrapper(worry_level):
            """
            The intermediate function that constructs arguments for the actual computing function.
            :param worry_level: `int` or `dict`
            :return: same as `worry_level`
            """
            # The function constructs a list of arguments for `func` to compute by substituting "old" in the template
            # with the given value of worry level
            args = [worry_level if x == 'old' else int(x) for x in inp]
            return func(args)

        return wrapper


def add(args):
    """
    Add together the contents of `args`
    :param args: `int` or `dict`
    :return: same as the first element of `args`
    """
    if isinstance(args[0], int):
        return sum(args)
        # This block is triggered in the relaxed mode of the game

    for divisor in args[0]:
        new_remainder = (args[0][divisor] + args[1]) % divisor
        args[0][divisor] = new_remainder
        # increase the remainder for each divisor from every monkey by the added amount and register the new
        # resulting remainder
    return args[0]


def multiply(args):
    """
    Return the product of the elements of `args`
    :param args: `int` or `dict`
    :return: same as the first element of `args`
    """
    if isinstance(args[0], int):
        return prod(args)
        # This block is triggered in the relaxed mode of the game

    if isinstance(args[1], int):
        args[1] = {divisor: args[1] for divisor in Monkey.divisors}
        # If the second multiplier is an `int`, multiply each remainder ny this `int`, just like in `add()`

    for divisor in args[0]:
        new_remainder = (args[0][divisor] * args[1][divisor]) % divisor
        args[0][divisor] = new_remainder
        # Otherwise multiply each remainder correspondingly
    return args[0]


with open('input11.txt') as f:
    data = f.read().rstrip()
puzzle = [[y.strip() for y in x.split('\n')] for x in data.split('\n\n')]

for raw_monkey in puzzle:
    items = raw_monkey[1].removeprefix('Starting items: ')
    operation = raw_monkey[2].removeprefix('Operation: new = ')
    divisor = raw_monkey[3].removeprefix('Test: divisible by ')
    true = raw_monkey[4].removeprefix('If true: throw to monkey ')
    false = raw_monkey[5].removeprefix('If false: throw to monkey ')
    Monkey(items, operation, divisor, true, false)
Monkey.activate()

for _ in range(20): Monkey.play_round()
print(prod(sorted(Monkey.items_inspected())[-2:]))

Monkey.reset()
for i in range(10000):
    Monkey.play_round(False)
print(prod(sorted(Monkey.items_inspected())[-2:]))
