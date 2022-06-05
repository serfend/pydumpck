import math
from pydumpck import logger
from typing import List
import time
import pydumpck.pyc_checker.lib_pycdc
import pydumpck.pyc_checker.lib_pycdc.build
import os
import pytest
import shutil


def handle_single(counter: List):
    if pydumpck.pyc_checker.lib_pycdc.use_pycdc():
        counter[1] += 1
    counter[0] += 1


def check_bin_exist():
    bin_path = pydumpck.pyc_checker.lib_pycdc.get_bin_path()
    exist = os.path.exists(bin_path)
    return bin_path, exist


def clear_previous_pycdc():
    bin_path, exist = check_bin_exist()
    pydumpck.pyc_checker.lib_pycdc.build.remove_cache()
    if exist:
        logger.debug(f'pycdc exists:{bin_path},remove it.')
        os.remove(bin_path)
    pydumpck.pyc_checker.lib_pycdc.build.remove_cache()
    _, exist = check_bin_exist()
    assert exist == False


@pytest.mark.skipif(os.name == 'nt', reason='windows doesn\'t need compile')
def test_pycdc_compile_single_time():
    clear_previous_pycdc()
    is_build = pydumpck.pyc_checker.lib_pycdc.use_pycdc()
    assert is_build == True, 'first time should run compile'
    is_build = pydumpck.pyc_checker.lib_pycdc.use_pycdc()
    assert is_build == False, 'second time should be use cache'
    _, exist = check_bin_exist()
    assert exist, True


@pytest.mark.skipif(os.name == 'nt', reason='windows doesn\'t need compile')
def test_pycdc_compile_multi_times():
    clear_previous_pycdc()
    from concurrent.futures import ThreadPoolExecutor
    thread_create_count = 10
    timeout_length = 120  # 120 second , for sometime run so slow

    threads = ThreadPoolExecutor(max_workers=thread_create_count)
    counter = [0, 0]
    for i in range(thread_create_count):
        threads.submit(handle_single, counter)
    start_time = time.time()
    while True:
        c = time.time() - start_time
        c = math.ceil(c*10) / 10
        if c > timeout_length:
            break
        if counter[0] >= thread_create_count:
            break
        logger.debug(f'waiting compiling...{c}')
        time.sleep(1)
    assert counter[1] > 0, f'no compile action is called.counter:{counter}'
    assert counter[1] == 1, f'more than one compiler is run.counter:{counter}'
    assert counter[
        0] >= thread_create_count, f'not all tasks completed in time.counter:{counter}'
    _, exist = check_bin_exist()
    assert exist, True
