"""
A* Algorithm is implemented in this file.
Algorithm uses State class for operations.
"""

from state import State
from copy import deepcopy
from typing import List, Tuple, Optional
from common import *
import heapq
import numpy as np


def a_star(state: State) -> Optional[State]:
    if not state.is_solvable:
        return None

    pri_q: List[Tuple[int, int, State, int]] = []
    closed: List[np.array] = []
    closed_parent: List[int] = []
    heapq.heappush(pri_q, (state.this_dist, 0, state, -1))
    while len(pri_q) != 0:
        curr: Tuple[int, int, State, int] = heapq.heappop(pri_q)
        g_score: int = curr[1] + 1
        st_check: np.array = curr[2].this_state.take(0, axis=2).flatten()
        if check_if_closed(st_check, closed) or g_score > 31:
            continue
        closed.append(st_check)
        closed_parent.append(curr[3])
        for i in range(4):
            in_state: State = deepcopy(curr[2])
            if not in_state.gen_next_state(i):
                break
            if in_state.get_distance() == 0:
                print_all(curr[3], in_state.this_state.take(0, axis=2).flatten(), st_check, closed, closed_parent)
                return in_state
            check_if_closed(in_state.this_state.take(0, axis=2).flatten(), closed)
            f_score: int = in_state.this_dist + g_score
            heapq.heappush(pri_q, (f_score, g_score, in_state, len(closed) - 1))
    return None


def check_if_closed(state, closed) -> bool:
    for j in range(len(closed)):
        if np.all(state == closed[j]):
            return True


def print_all(p_count: int, state_flat: np.array,
              previous_flat: np.array, closed: List[np.array], closed_parent: List[int]) -> None:
    print_helper(state_flat)
    print_helper(previous_flat)
    while p_count > -1:
        print_helper(closed[p_count])
        p_count = closed_parent[p_count]
