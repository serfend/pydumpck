import os
from typing import List
from pydumpck.pyinstaller_dump import run
from .common import res_type
import pydumpck.configuration
import pydumpck.pyc_checker.extensions
import sys
import shutil
def start_run():
    print('params', sys.argv)
    return run()

def check_uncompile_files(target_file: str):
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_pycdc_path(
        target_file)), 'pycdc-result not found'
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_uncompyle6_path(
        target_file)), 'uncompyle6-result not found'


def check_files(specify_files_outer: List, specify_files_inner: List):
    output = f'{pydumpck.configuration.thread_output_directory}'
    output = os.path.abspath(output)
    print(f'test output:{output}')
    assert os.path.exists(output)
    output = f'{output}{os.path.sep}'
    for i in specify_files_outer:
        check_uncompile_files(f'{output}{i}.pyc')
    extract_dir = 'PYZ-00.pyz_extract'
    pyz_output = f'{output}{extract_dir}'
    print(f'test pyz_output:{pyz_output}')
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


def test_version():
    sys.argv = [sys.argv[0], '-v']
    result = start_run()
    import pydumpck.__version__
    assert result == pydumpck.__version__.__version__
