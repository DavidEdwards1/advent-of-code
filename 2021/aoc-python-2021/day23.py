from collections import namedtuple
from dataclasses import dataclass
from os import stat
from typing import Tuple

@dataclass(frozen=True)
class State:
    ends: Tuple
    mids: Tuple
    rooms: Tuple

def between(start, end, mid):
    if start == "Left" and end == "A":
        return False
    elif end == "Left" and start == "A":
        return False
    elif start == "Left" and end == "B" and mid == "AB":
        return True
    elif end == "Left" and start == "B" and mid == "AB":
        return True

def room_moves(state):
    """
    Moves from rooms
    """
    destination_states = []

    for r, amphipods in state.rooms:
        if len(amphipods) == 0:
            continue

        amphipod = amphipods[-1]

        # check if in own room and room doesn't havve others
        if amphipod == r and (all(o == amphipod for o in amphipods)):
            continue

        # check to see if can move to own room:
        own_room = list(filter(lambda r: r[0] == amphipod, state.rooms))[0]

        if all(o == amphipod for o in own_room[1]):
            new_rooms = []
            for room, current_occupants in state.rooms:
                if room == r:
                    new_room = (room, current_occupants[:-1])
                elif room == amphipod:
                    new_room = (room, (*current_occupants, amphipod))
                else:
                    new_room = (room, current_occupants)
                new_rooms.append(new_room)
            new_rooms = tuple(new_rooms)

            destination_states.append(
                (State(
                    state.ends,
                    state.mids,
                    new_rooms
                ), 1)
            )

        # check if hallway ends are empty
        if len(state.ends[0][1]) < 2:
            # can move to left end?
            # if room is A, then always yes
            intervening_mids = [(mid, occupier) for mid, occupier in state.mids if between(r, "Left", mid)]

            if all(occupier is None for mid, occupier in intervening_mids):
                new_rooms = tuple(
                    (room, current_occupants[:-1]) if room == r else (room, current_occupants)
                    for room, current_occupants in state.rooms
                )
                destination_states.append(
                    (State(
                        (("Left", (*state.ends[0][1], amphipod)), ("Right", state.ends[1][1])),
                        state.mids,
                        new_rooms
                    ), 1)
                )

        if len(state.ends[1][1]) < 2:
            # can move to right end?
            # if room is B, then always yes
            intervening_mids = [(mid, occupier) for mid, occupier in state.mids if between(r, "Left", mid)]

            if all(occupier is None for mid, occupier in intervening_mids):
                new_rooms = tuple(
                    (room, current_occupants[:-1]) if room == r else (room, current_occupants)
                    for room, current_occupants in state.rooms
                )
                destination_states.append(
                    (State(
                        (("Left", state.ends[0][1]), ("Right", (*state.ends[1][1], amphipod))),
                        state.mids,
                        new_rooms
                    ), 1)
                )

    return destination_states

def hallway_moves(state):
    destination_states = []

    for e, amphipods in state.ends:
        if len(amphipods) == 0:
            continue

        amphipod = amphipods[-1]
        # check to see if can move to own room:
        own_room = list(filter(lambda r: r[0] == amphipod, state.rooms))[0]

        if all(o == amphipod for o in own_room[1]):
            new_rooms = []
            for room, current_occupants in state.rooms:
                if room == amphipod:
                    new_room = (room, (*current_occupants, amphipod))
                else:
                    new_room = (room, current_occupants)
                new_rooms.append(new_room)
            new_rooms = tuple(new_rooms)

            new_ends = []
            for end, current_occupants in state.ends:
                if end == e:
                    new_end = (end, current_occupants[:-1])
                else:
                    new_end = (end, current_occupants)
                new_ends.append(new_end)
            new_ends = tuple(new_ends)

            destination_states.append(
                (State(
                    new_ends,
                    state.mids,
                    new_rooms
                ), 1)
            )
    return destination_states

edges = {}
visted_states = set()
states_to_consider = [State(
    (("Left", ()), ("Right", ())),
    (("AB", None),),
    (("A", ("A","B")),("B", ("A","B"))),
)]

solved_state = State(
    (("Left", ()), ("Right", ())),
    (("AB", None),),
    (("A", ("A","A")),("B", ("B","B"))),
)

i = 0
while states_to_consider:
    state = states_to_consider.pop()
    print(f"Looking for new states from: {state}")

    if state == solved_state:
        all_destinations = []
    else:
        # generate moves from rooms
        room_move_destinations = room_moves(state)
        # generate moves from hallway
        hallway_move_destinations = hallway_moves(state)

        all_destinations = room_move_destinations + hallway_move_destinations

    edges[state] = all_destinations
    states_to_consider.extend([new_state for new_state,cost in all_destinations if new_state not in visted_states])
    visted_states.update([state])

    print("States to look at: ", states_to_consider)
    print("Visited States: ", visted_states)
    i += 1
    # if i == 4: break

for state, moves in edges.items():
    print("Starting State: ", state)
    for move, cost in moves:
        print(f" -- Possible Move: {move}, Cost: {cost}")
