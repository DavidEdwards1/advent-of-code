from toolz.functoolz import curry, pipe
from toolz.dicttoolz import assoc, assoc_in

@curry
def inp(a, state):
    read_pos = state["input"]["read_pos"]
    new_state = assoc(state, a, state["input"]["buffer"][read_pos])
    new_state = assoc_in(new_state, ["input", "read_pos"], read_pos + 1)
    return new_state

def apply_bin_op(op, a,b,state):
    if isinstance(b, int):
        new_state = assoc(state, a, op(state[a], b))
    else:
        new_state = assoc(state, a, op(state[a], state[b]))
    return new_state

@curry
def add(a,b, state):
    op = lambda x,y: x + y
    return apply_bin_op(op, a,b,state)

@curry
def mul(a,b, state):
    op = lambda x,y: x * y
    return apply_bin_op(op, a,b,state)

@curry
def div(a,b, state):
    op = lambda x,y: x // y
    return apply_bin_op(op, a,b,state)

@curry
def mod(a,b, state):
    op = lambda x,y: x % y
    return apply_bin_op(op, a,b,state)

@curry
def eql(a,b, state):
    op = lambda x,y: int(x == y)
    return apply_bin_op(op, a,b,state)


def parse_input(filename):
    with open(filename) as f:
        instructions = [l.strip().split(" ") for l in f.readlines()]

    ops = {
        "inp": inp,
        "add": add,
        "mul": mul,
        "div": div,
        "mod": mod,
        "eql": eql
    }

    instructions = [
        [inst[0], inst[1], int(inst[2])] if (len(inst)==3) and inst[2] not in ("w", "x", "y", "z")
        else inst
        for inst in instructions]

    instructions = [ops[inst[0]](*inst[1:]) for inst in instructions]

    return instructions

def evaluate(program, state):
    return pipe(state, *program)


if __name__ == "__main__":
    program = parse_input("data-day24-example4.txt")

    for i in range(1,10):
        state = {
            "w": 0, "x": 0, "y": 0, "z": 0,
            "input": {
                "buffer": [i],
                "read_pos": 0
            }
        }


        result = evaluate(program, state)

        print(result)
