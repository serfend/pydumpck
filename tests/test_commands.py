from pydumpck import logger
import os
from typing import List
from pydumpck.pyinstaller_dump import run
from .common import res_type
import pydumpck.configuration
import pydumpck.pyc_checker.extensions
import sys
import shutil
import pytest


def start_run():
    logger.info(f'params:{sys.argv}')
    return run()


def check_uncompile_files(target_file: str):
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_pycdc_path(
        target_file)), 'pycdc-result not found'
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_uncompyle6_path(
        target_file)), 'uncompyle6-result not found'


def check_files(specify_files_outer: List, specify_files_inner: List):
    output = f'{pydumpck.configuration.thread_output_directory}'
    output = os.path.abspath(output)
    logger.debug(f'test output:{output}')
    assert os.path.exists(output)
    output = f'{output}{os.path.sep}'
    for i in specify_files_outer:
        check_uncompile_files(f'{output}{i}.pyc')
    extract_dir = 'PYZ-00.pyz_extract'
    pyz_output = f'{output}{extract_dir}'
    logger.debug(f'test pyz_output:{pyz_output}')
    assert os.path.exists(pyz_output)
    pyz_output = f'{pyz_output}{os.path.sep}'
    for i in specify_files_inner:
        check_uncompile_files(f'{pyz_output}{i}.pyc')
    shutil.rmtree(output)


def test_commands_elf():
    elf = res_type.get_res('elf')
    args = [
        elf[0],
        "--plugin",
        "pycdc",
        "uncompyle6",
        "--decompile_file",
        "main",
        "squid",
        "squid_game"
    ]
    sys.argv = [sys.argv[0]] + args
    start_run()
    check_files(['squid'], ['squid_game'])


def test_no_input():
    sys.argv = [sys.argv[0]]
    start_run()


def test_absolute_path():
    elf = res_type.get_res('elf')
    absolute_path = f'{os.path.sep}tmp{os.path.sep}' if os.name == 'posix' else f'C:{os.path.sep}Windows{os.path.sep}Temp{os.path.sep}'
    absolute_path += pydumpck.utils.paths.get_random_path('test')
    shutil.copy(elf[0], absolute_path)
    args = [
        absolute_path,
        "--plugin",
        "pycdc",
        "uncompyle6",
        "--decompile_file",
        "main",
        "squid",
        "squid_game"
    ]
    sys.argv = [sys.argv[0]] + args
    start_run()
    check_files(['squid'], ['squid_game'])
    os.remove(absolute_path)


def test_version():
    sys.argv = [sys.argv[0], '-v']
    result = start_run()
    import pydumpck.__version__
    assert result == pydumpck.__version__.__version__
