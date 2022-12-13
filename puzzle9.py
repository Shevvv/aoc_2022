class Rope:

    litteras = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
    }

    def __init__(self, followers):
        self.head = (0, 0)
        self.tail = (0, 0)
        self.trail = {(0, 0)}
        self.follower = FollowerRope(followers - 1) if followers > 0 else None
        # self.number = 8 - followers + 1

    def pull_tail(self):
        relative_head = (self.head[0] - self.tail[0], self.head[1] - self.tail[1])
        if 2 in (abs(relative_head[0]), abs(relative_head[1])):
            x = int(self.tail[0] + relative_head[0] / abs(relative_head[0])) if relative_head[0] != 0 else self.tail[0]
            y = int(self.tail[1] + relative_head[1] / abs(relative_head[1])) if relative_head[1] != 0 else self.tail[1]
            self.tail = (x, y)

    def move_head_consequences(self):
        self.pull_tail()
        self.trail.add(self.tail)
        # print(f'number: {self.number}, head: {self.head}, tail: {self.tail}; ', end='')

        if self.follower:
            self.follower.move_head(self.tail)
        # else:
        #     print()


class HeadRope(Rope):

    def __init__(self, followers=0):
        super().__init__(followers)

    def move_head(self, littera, dist):
        direction = self.litteras[littera]
        for _ in range(int(dist)):
            x = self.head[0] + direction[0]
            y = self.head[1] + direction[1]
            self.head = (x, y)
            self.move_head_consequences()


class FollowerRope(Rope):

    def __init__(self, followers=0):
        super().__init__(followers)

    def move_head(self, head):
        self.head = head
        self.move_head_consequences()


with open('input9.txt') as f:
    data = f.read().rstrip()
puzzle = [x.split() for x in data.split('\n')]

followers = 8
rope = HeadRope(followers)
for move in puzzle:
    rope.move_head(*move)

curr_rope = rope
for _ in range(followers):
    curr_rope = curr_rope.follower
print(len(rope.trail))
print(len(curr_rope.trail))
