import os
import pydumpck.pyinstaller_dump
from .common import res_type
import pydumpck.configuration
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
    output = pydumpck.configuration.thread_output_directory
    assert os.path.exists(f'{output}')
    assert os.path.exists(f'{output}/squid.pyc.py')
    assert os.path.exists(f'{output}/squid.pyc.py.up6.py')
    extract_dir = 'PYZ-00.pyz_extract'
    assert os.path.exists(f'{output}/{extract_dir}')
    assert os.path.exists(f'{output}/{extract_dir}/squid_game.pyc.py')
    assert os.path.exists(f'{output}/{extract_dir}/squid_game.pyc.py.up6.py')
    shutil.rmtree(output)

