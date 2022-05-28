from argparse import ArgumentError
from typing import Callable, List

from sympy import E


def find(arr: List, predict: Callable):
    c_count = predict.__code__.co_argcount
    if c_count == 1:
        def predict(index, i): return predict(i)
    elif c_count == 2:
        pass
    else:
        raise ArgumentError(f'invalid param count {c_count}')
    for index, i in enumerate(arr):
        if predict(index, i):
            return i
