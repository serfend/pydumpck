from typing import Callable, Dict, List, Tuple
from . import resources
import pytest


def get_res(t: str):
    res = resources[t]
    if isinstance(res, str):
        file_path = res
        target_type = t
        deompile_files = None
    elif isinstance(res, Tuple):
        file_path = res[0]
        target_type = res[1]
        deompile_files = res[2] if len(res) > 2 else None
    else:
        assert 'invalid resources' == t, f'resouece invalid'
    return (file_path, target_type, deompile_files)


def resources_filter(resoueces: Dict, keys: List):
    r = {}
    for k in keys:
        if not k in resoueces:
            continue
        r[k] = resoueces[k]
    return r


resources_arch = resources_filter(
    resources, ['exe-3.10', 'exe-3.10-v2', 'exe-encrypt', 'elf', 'pyz'])


@pytest.fixture(scope='function', params=list(resources))
def res_type_all(request: pytest.FixtureRequest):
    p = request.param
    yield get_res(p)


@pytest.fixture(scope='function', params=list(resources_arch))
def res_type_arch(request: pytest.FixtureRequest):
    p = request.param
    yield get_res(p)
