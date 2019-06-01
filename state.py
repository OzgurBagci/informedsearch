"""
In this file, the class for graph nodes are defined.
It is called state since I thought it suits better for our use case.
"""

from typing import List, Tuple
import numpy as np


UP = 1
DOWN = -1
LEFT = 10
RIGHT = -10


class State:
    this_state: np.array
    this_dist: int
    blank_coord: Tuple[int, int]
    is_solvable: bool

    def __init__(self,
                 _2d_curr: List[Tuple[int, int, int]],
                 _2d_goal: List[Tuple[int, int, int]]):
        arr: List[List[List[int, int, int]]] = [[], [], []]
        for i in range(3):
            for j in range(3):
                curr: int = _2d_curr[i][j]
                curr_moves: List[int, int, int] = [curr, 0, 0]
                arr[i].append(curr_moves)
                if curr == 0:
                    self.blank_coord = j, i
                else:
                    self.find_distance(curr, _2d_goal, i, j, curr_moves)
        self.this_state = np.array(arr)
        self.set_distance()
        self.solution_check(_2d_goal)

    def find_distance(self, curr, _2d_goal, i, j, curr_moves):
        for k in range(3):
            for l in range(3):
                if _2d_goal[k][l] == curr:
                    curr_moves[1] += ((i - k) * UP)
                    curr_moves[2] += ((j - l) * LEFT)
                    return

    def set_distance(self):
        self.this_dist = int(np.absolute(self.this_state.take(1, axis=2).flatten()).sum() +
                             np.absolute(self.this_state.take(2, axis=2).flatten()).sum() / 10)

    def get_distance(self) -> int:
        return self.this_dist

    def gen_next_state(self, th: int = 0) -> bool:
        """
        :param th: In order of shortest distance to longest which should be generated. 0 is the shortest...
        """
        next_states: List[Tuple[int, int]] = []
        for dirr, ch_x, ch_y in [(1, 0, 1), (-1, 0, -1), (10, 1, 0), (-10, -1, 0)]:

            val = self.this_state[self.blank_coord[1] - ch_y][self.blank_coord[0] - ch_x] \
                if 2 >= self.blank_coord[1] - ch_y >= 0 and 2 >= self.blank_coord[0] - ch_x >= 0 else None

            dist: int = int(abs(val[1]) + abs(val[2]) / 10 - abs(val[1] + ch_y) - abs(val[2] / 10 + ch_x)) \
                if val is not None else -100

            next_states.append((dist, dirr))

        next_states = sorted(next_states, reverse=True, key=lambda x: x[0])

        if next_states[th][0] == -100:
            return False

        self.swap(next_states[th][1])
        self.this_dist -= next_states[th][0]

        return True

    def swap(self, to: int) -> None:
        """
        :param to: LEFT, RIGHT, UP OR DOWN... Hint: LEFT is for Blank to shift to left.
        """
        b_x = self.blank_coord[0]
        b_y = self.blank_coord[1]
        to_cell = 1
        move_ver = to
        move_hor = 0

        if to == LEFT or to == RIGHT:
            move_hor = int(to / 10)
            move_ver = 0
            to_cell = 2

        self.this_state[b_y - move_ver][b_x - move_hor][to_cell] += to

        tmp = np.array(self.this_state[b_y, b_x], copy=True)
        self.this_state[b_y, b_x] = self.this_state[b_y - move_ver, b_x - move_hor]
        self.this_state[b_y - move_ver, b_x - move_hor] = tmp

        self.blank_coord = (b_x - move_hor, b_y - move_ver)

    def solution_check(self, solution: List[Tuple[int, int, int]]) -> None:
        inversions: int = 0
        flat_array: np.array = self.this_state.take(0, axis=2).flatten()
        flat_solution = np.array(solution).flatten()
        for i in range(8):
            for j in range(i, 9):
                if flat_array[i] and flat_array[j] and \
                        np.where(flat_solution == flat_array[i])[0][0] > np.where(flat_solution == flat_array[j])[0][0]:
                    inversions += 1

        self.is_solvable = inversions % 2 == 0

    def __lt__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return self.this_dist < other.this_dist
