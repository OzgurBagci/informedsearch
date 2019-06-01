"""
Common functions which are used by both of the algorithms.
"""
import numpy as np


def print_helper(arr: np.array):
    pr_str = ''
    for i in range(9):
        pr_str += str(arr[i]) + ' '
        if (i + 1) % 3 == 0:
            pr_str += '\n'
    print(pr_str)
