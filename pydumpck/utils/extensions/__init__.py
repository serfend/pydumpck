from argparse import ArgumentError
from typing import Callable, List


def find(arr: List, predict: Callable) -> any:
    c_count = predict.__code__.co_argcount
    if c_count == 1:
        def x_predict(i, index): return predict(i)
    elif c_count == 2:
        x_predict = predict
    else:
        raise ArgumentError(message = f'invalid param count {c_count}')
    for index, i in enumerate(arr):
        if x_predict(i, index):
            return i
    return None


def flat(arr: List, rank: int = 1) -> List:
    if rank <= 0:
        return arr
    result = []
    for i in arr:
        result += flat(i, rank-1)
    return result


def distinct(arr: List, predict: Callable = None) -> List:
    '''
    distinct a array
    arr     :   List[T]
    predict :   Callable[T,str]
    '''
    if not predict:
        def predict(x): return x
    dic = {}
    result = []
    for i in arr:
        k = predict(i)
        if k in dic:
            continue
        dic[k] = True
        result.append(i)
    return result
