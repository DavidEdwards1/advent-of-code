def deterministic_dice(n_rolls, start, max):
    """
    n_rolls: The number of rolls that happen in one turn
    """
    # start at start - 1 and then add 1 on afterwards
    # to account for the properties of mod
    return sum(x%max + 1 for x in range(start-1,start+n_rolls-1))

def update_game_state(game_state, possible_moves, player_to_update):
    """
    player_to_update: is it the first or second player to update state for, zero indexed
    """
    new_game_state = {}
    for state, count in game_state.items():
        for moves, move_counts in possible_moves.items():
            if player_to_update == 0:
                start_pos = state[2]
                new_pos = move_places(start_pos, moves)

                new_count = count * move_counts
                new_state = (state[0]+new_pos, state[1], new_pos, state[3])
            else:
                start_pos = state[3]
                new_pos = move_places(start_pos, moves)

                new_count = count * move_counts
                new_state = (state[0], state[1]+new_pos, state[2], new_pos)

            if new_state in new_game_state:
                new_game_state[new_state] = new_game_state[new_state] + new_count
            else:
                new_game_state[new_state] = new_count

    return new_game_state

def move_places(start, places_to_move):
    return (start - 1 + places_to_move) % 10 + 1

def winning_state(state, winning_score):
    return (state[0] >= winning_score) or (state[1] >= winning_score)




n_rolls = 3

player_1_wins = False
player_2_wins = False

die_start, die_max = 1, 100

total_die_rolls = 0

game_state = {(0,0, 8,4): 1}

while True:
    # update player 1
    possible_moves = {deterministic_dice(n_rolls, die_start, die_max): 1}
    die_start += 3
    total_die_rolls += 3
    game_state = update_game_state(game_state, possible_moves, 0)
    winning_states = {state: count for state,count in game_state.items() if winning_state(state, 1000)}

    if winning_states:
        player_1_wins = True
        losing_score = list(winning_states.keys())[0][1]
        break

    # update player 2
    possible_moves = {deterministic_dice(n_rolls, die_start, die_max): 1}
    die_start += 3
    total_die_rolls += 3
    game_state = update_game_state(game_state, possible_moves, 1)
    winning_states = {state: count for state,count in game_state.items() if winning_state(state, 1000)}

    if winning_states:
        player_2_wins = True
        losing_score = list(winning_states.keys())[0][0]
        break

print("Losing Score is: ", losing_score)
print("Number of dice rolls: ", total_die_rolls)
print("Multiplied together: ", losing_score*total_die_rolls)

# part 2
possible_moves = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
game_state = {(0,0, 8, 4): 1}

winning_states = {}

while game_state:
    # update player 1
    game_state = update_game_state(game_state, possible_moves, 0)
    print("total states:", sum(game_state.values()))
    new_winning_states = {state: count for state,count in game_state.items() if winning_state(state, 21)}

    for state, count in new_winning_states.items():
        if state in winning_states:
            winning_states[state] += count
        else:
            winning_states[state] = count

    for state in new_winning_states:
        game_state.pop(state)

    # update player 2
    game_state = update_game_state(game_state, possible_moves, 1)
    print("total states:", sum(game_state.values()))
    new_winning_states = {state: count for state,count in game_state.items() if winning_state(state, 21)}

    for state in new_winning_states:
        game_state.pop(state)

    for state, count in new_winning_states.items():
        if state in winning_states:
            winning_states[state] += count
        else:
            winning_states[state] = count

player_1_wins = 0
player_2_wins = 0

print(sum(winning_states.values()))

for state, count in winning_states.items():
    if state[0] > state [1]: player_1_wins += count
    else: player_2_wins += count


print("Player one wins: ", player_1_wins)
print("Player two wins: ", player_2_wins)
