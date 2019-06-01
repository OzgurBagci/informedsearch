"""
Input and output file creation functions and main part are implemented in this file.
To run, just type "python3 main.py" into the Console.
"""
import sys
from state import State
from typing import Tuple, List
from idastar import ida_star
from astar import a_star


def take_input() -> State:
    with open('input.txt', 'r') as input_file:
        goal: List[Tuple[int, int, int]] = []
        for _ in range(3):
            goal.append(tuple(map(lambda x: int(x), input_file.readline().split())))

        input_file.readline()

        initial: List[Tuple[int, int, int]] = []
        for _ in range(3):
            initial.append(tuple(map(lambda x: int(x), input_file.readline().split()))
                           )
    return State(initial, goal)


if __name__ == '__main__':
    print('Running...')
    state: State = take_input()
    sys.stdout = open('outputA.txt', 'w')
    res = a_star(state)
    if res is None:
        print('fail')
    sys.stdout = open('outputIDA.txt', 'w')
    res = ida_star(state)
    if res is None:
        print('fail')
