from typing import List, final

import numpy as np


def row_to_ints(row: List[str]) -> List[int]:
    return [int(x) for x in row]

def score(board, unmarked_mask, n):
    return (board * unmarked_mask).sum() * n


with open("data-day04.txt") as f:
    numbers_called = [int(s) for s in f.readline().strip().split(",")]

    # read rest of lines as all of them are about boards
    boards_string = f.readlines()

boards = []

for i in range(len(boards_string)//6):
    board_start = i * 6 + 1
    board_end = (i+1) * 6

    board = [row_to_ints(row.strip().split()) for row in boards_string[board_start:board_end]]
    boards.append(board)

boards = np.array(boards)

marked_mask = np.zeros(boards.shape)

winning_boards = {}
winning_board_order = []

for n in numbers_called:
    marked_mask = marked_mask + (boards == n)
    unmarked_mask = ~(marked_mask.astype(bool))

    # check for winning board
    completed_cols = marked_mask.sum(axis=1) == 5
    completed_rows = marked_mask.sum(axis=2) == 5

    winning_states_for_board = completed_rows.sum(axis=1) + completed_cols.sum(axis=1)

    for b in np.where(winning_states_for_board >= 1)[0]:
        if b not in winning_boards:
            winning_boards[b] = {
                "board": boards[b],
                "unmarked": unmarked_mask[b].copy(),
                "number_called": n,
            }
            winning_board_order.append(b)

first_winning_board = winning_boards[winning_board_order[0]]
last_winning_board = winning_boards[winning_board_order[-1]]

print("First Winning Board: ", winning_board_order[0])
print(
    "   -- Score        : ",
    score(
        first_winning_board["board"],
        first_winning_board["unmarked"],
        first_winning_board["number_called"]
    )
)

print("Last Winning Board: ", winning_board_order[-1])
print(
    "   -- Score        : ",
    score(
        last_winning_board["board"],
        last_winning_board["unmarked"],
        last_winning_board["number_called"]
    )
)
