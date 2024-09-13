from typing import Tuple


def raw_input_to_point(inp: str) -> Tuple[int]:
    inp = inp.strip().split(",")
    return (int(inp[0]), int(inp[1]))

def raw_input_to_instruction(inp: str) -> Tuple[str, int]:
    inp = inp[10:].strip().split("=")
    return (inp[0], int(inp[1]))


with open("data-day13.txt") as f:
    points = [raw_input_to_point(f.readline())]

    while points[-1] != "":
        if line := f.readline().strip():
            points.append(raw_input_to_point(line))
        else:
            break

    instructions = [raw_input_to_instruction(l) for l in f.readlines()]

points = set(points)

for i, inst in enumerate(instructions):

    if inst[0] == "y":
        # then fold up so y x coord stays the same
        # but y changes such that distance to fold stays constant
        y_fold = inst[1]
        points = set((p[0], y_fold - abs(p[1] - y_fold)) for p in points)
    elif inst[0] == "x":
        # fold left side on to right so that x coord stays the same
        # I think this is the same as folding right overall
        # but x changes such that distance to fold is constant
        x_fold = inst[1]
        points = set((x_fold - abs(p[0] - x_fold), p[1]) for p in points)

    print(f"After instruction {i}, {inst} there are: {len(points)} points")

max_x = max(p[0] for p in points)
max_y = max(p[1] for p in points)

output = []

for j in range(max_y+1):
    row = []
    for i in range(max_x+1):
        row.append("#" if (i,j) in points else ".")
    row = "".join(row)
    output.append(row)

print("\nOutput code is:")
print("\n".join(output))
