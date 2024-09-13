import numpy as np


def make_line(line_string: str):
    return line_string.split("->")

class Line:
    def __init__(self, start, stop) -> None:
        self.start = start
        self.stop = stop

    @property
    def type(self):
        if self.start[0] == self.stop[0]:
            ans = "horizontal"
        elif self.start[1] == self.stop[1]:
            ans = "vertical"
        else:
            ans = "diagonal"

        return ans

    @property
    def minx(self):
        return min(self.start[0], self.stop[0])

    @property
    def maxx(self):
        return max(self.start[0], self.stop[0])

    @property
    def miny(self):
        return min(self.start[1], self.stop[1])

    @property
    def maxy(self):
        return max(self.start[1], self.stop[1])

    @property
    def points(self):
        if self.type == "horizontal":
            points = [[self.start[0], i] for i in range(self.miny, self.maxy+1)]
        elif self.type == "vertical":
            points = [[i, self.start[1]] for i in range(self.minx, self.maxx+1)]
        else:
            # we don't know the direction of the diagonal so work out the step
            x_step = 1 if self.start[0] < self.stop[0] else -1
            y_step = 1 if self.start[1] < self.stop[1] else -1
            points = [
                [self.start[0]+(x_step*i), self.start[1]+(y_step*i)]
                for i in range(self.maxy+1-self.miny)
            ]

        return points

    def __repr__(self) -> str:
        return f"Line: start={self.start}, stop={self.stop}, type={self.type}"

    @classmethod
    def from_string(klass, string):
        start, stop = string.split("->")

        start = [int(x) for x in start.strip().split(",")]
        stop = [int(x) for x in stop.strip().split(",")]

        return Line(start, stop)

def calculate_vent_map(lines, line_filter):
    # since Python is zero indexed, if we have to get to point (9,9) we need a
    # 10x10 grid
    max_xy = (max(l.maxx for l in lines)+1, max(l.maxy for l in lines)+1)
    vent_map = np.zeros(max_xy)

    for l in lines:
        if not line_filter(l): continue
        for p in l.points:
            x,y = p[1],p[0] # this swap is really for debugging, prints out map same orientation as given on website
            vent_map[x,y] = vent_map[x,y] + 1

    return vent_map


with open("data-day05.txt") as f:
    lines = [Line.from_string(l) for l in f.readlines()]

print(
    "Challenge One Danger Points: ",
    np.sum(
        calculate_vent_map(lines, lambda l: l.type in ("vertical", "horizontal")
    ) >= 2)
)

print(
    "Challenge Two Danger Points: ",
    np.sum(
        calculate_vent_map(lines, lambda l: True) >= 2)
)
