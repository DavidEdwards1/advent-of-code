import functools
import json

def magnitude(sf_num):
    left, right = sf_num
    if isinstance(left, int):
        left_mag = left
    else:
        left_mag = magnitude(left)

    if isinstance(right, int):
        right_mag = right
    else:
        right_mag = magnitude(right)

    return 3 * left_mag + 2 * right_mag

def split(sf_num):
    left, right = sf_num

    if isinstance(left, int):
        if left >= 10 :
            left = [left // 2, left - (left // 2)]
            has_split_left = True
        else:
            has_split_left = False
    else:
        left, has_split_left = split(left)

    if not has_split_left:
        if isinstance(right, int):
            if right >= 10:
                right = [right // 2, right - (right // 2)]
                has_split_right = True
            else:
                has_split_right = False
        else:
            right, has_split_right = split(right)

    return [left, right], (has_split_left or has_split_right)


def add_to_leftmost(sf_num, to_add):
    left, right = sf_num

    if isinstance(left, int):
        new_left = left+to_add
    else:
        new_left = add_to_leftmost(left, to_add)

    return [new_left, right]

def add_to_rightmost(sf_num, to_add):
    left, right = sf_num

    if isinstance(right, int):
        new_right = right+to_add
    else:
        new_right = add_to_rightmost(right, to_add)

    return [left, new_right]

def explode(sf_num, depth=0):
    left, right = sf_num
    left_has_exploded, right_has_exploded = False, False
    carry = [0, 0]

    if depth==3:
        if isinstance(left, list): # if so, nested too deep and explode it!
            # since it is the left node of this level, there is no regular
            # number to the left in this level so left of left is carried
            carry = left
            # we should always have a right, so we can add_to_leftmost the right
            left = 0
            left_has_exploded = True
        elif isinstance(right, list):
            carry = right
            right = 0
            right_has_exploded = True

    else:
        # now we recur, we have to recur down the left first, only once we have done
        # that can we look at the right
        # only recur if left/right is a list
        if isinstance(left, list):
            left, carry, left_has_exploded = explode(left, depth=depth+1)

        if not left_has_exploded and isinstance(right, list):
            right, carry, right_has_exploded = explode(right, depth=depth+1)

    # apply the carries
    if left_has_exploded and carry[1]:
        if isinstance(right, int):
            right, carry = right + carry[1], [carry[0],0]
        else:
            right, carry = add_to_leftmost(right, carry[1]), [carry[0],0]

    if right_has_exploded and carry[0]:
        if isinstance(left, int):
            left, carry = left + carry[0], [0, carry[1]]
        else:
            left, carry = add_to_rightmost(left, carry[0]), [0, carry[1]]


    return [left, right], carry, (left_has_exploded or right_has_exploded)


def reduce(sf_num):
    finished_reducing = False

    while not finished_reducing:
        sf_num, carry, has_exploded = explode(sf_num)
        if has_exploded: continue
        sf_num, has_split = split(sf_num)
        if has_split: continue

        finished_reducing = True

    return sf_num

def raw_add(sf_num1, sf_num2):
    return [sf_num1, sf_num2]

def add(sf_num1, sf_num2):
    return reduce(raw_add(sf_num1, sf_num2))

def add_list(sf_nums):
    return functools.reduce(
        add,
        sf_nums
    )


def read(filename):
    with open(filename) as f:
        sf_nums = [json.loads(n) for n in f.readlines()]

    return sf_nums

def solve(filename):
    return add_list(read(filename))

def pairwise_sums(sf_nums):
    pairwise = []
    for i, n in enumerate(sf_nums):
        pairwise.extend([add(n, other) for j, other in enumerate(sf_nums) if i != j])

    return pairwise

def solve_part_two(filename):
    sums = pairwise_sums(read(filename))

    return max(magnitude(n) for n in sums)

if __name__ == "__main__":
    sum_result = solve("data-day18.txt")

    print("Magnitude of sum: ", magnitude(sum_result))

    print("Max magnitude for adding two numbers: ", solve_part_two("data-day18.txt"))
