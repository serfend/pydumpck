import os
import pydumpck.pyinstaller_dump
from .common import res_type
import pydumpck.configuration
import pydumpck.pyc_checker.extensions
import sys
import shutil


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
    pydumpck.pyinstaller_dump.run()
    output = f'{pydumpck.configuration.thread_output_directory}'
    output = os.path.abspath(output)
    print(f'test output:{output}')
    assert os.path.exists(output)
    output = f'{output}{os.path.sep}'
    target_file = f'{output}squid.pyc'
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_pycdc_path(
        target_file)), 'pycdc on outer file not found'
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_uncompyle6_path(
        target_file)), 'uncompyle6 on outer file not found'
    extract_dir = 'PYZ-00.pyz_extract'
    pyz_output = f'{output}{extract_dir}'
    print(f'test pyz_output:{pyz_output}')
    assert os.path.exists(pyz_output)
    pyz_output = f'{pyz_output}{os.path.sep}'
    target_file = f'{pyz_output}squid_game.pyc'
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_pycdc_path(
        target_file)), 'pycdc on inner file not found'
    assert os.path.exists(pydumpck.pyc_checker.extensions.get_uncompyle6_path(
        target_file)), 'uncompyle6 on inner file not found'
    shutil.rmtree(output)
