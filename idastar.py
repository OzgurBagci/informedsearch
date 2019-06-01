"""
IDA* Algorithm is implemented in this file.
Algorithm uses State class for operations.
"""
from state import State
from typing import List, Tuple, Optional
from common import *
from copy import deepcopy
import numpy as np


def ida_star(state: State) -> Optional[State]:
    if not state.is_solvable:
        return None

    upper_bound = state.this_dist
    while True:
        res = search(state, 0, upper_bound, [])
        if res[0] == -1:
            return res[1]
        elif res[0] == 1000:
            return None
        upper_bound = res[0]


def search(state: State, g_val: int, upper_bound: int, previous: List[np.array]) -> Tuple[int, Optional[State]]:
    if g_val > 31:
        return 1000, None

    if state.get_distance() == 0:
        print_helper(state.this_state.take(0, axis=2).flatten())
        for arr in reversed(previous):
            print_helper(arr)
        return -1, state
    f_val = g_val + state.this_dist
    if f_val > upper_bound:
        return f_val, None
    min_val = 1000
    for i in range(4):
        in_state = deepcopy(state)
        if in_state.gen_next_state(i):
            previous_deep = deepcopy(previous)
            previous_deep.append(state.this_state.take(0, axis=2).flatten())
            res = search(in_state, g_val + 1, upper_bound, previous_deep)
            if res[0] == -1:
                return res
            min_val = min(min_val, res[0])
    return min_val, None
