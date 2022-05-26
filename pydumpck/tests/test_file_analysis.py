import os
from typing import Tuple
from .common import resources, current_path
import pydumpck.py_common_dump as dmp
import pydumpck.configuration as configuration
from .common.res_type import *
import shutil
import pydumpck.utils.paths


def start_arch_file(res_type_arch: Tuple):
    file_path, target_type = res_type_arch
    output_dir = f'{os.path.dirname(file_path)}{os.path.sep}{pydumpck.utils.paths.get_random_path("output")}'
    configuration.thread_output_directory = output_dir
    dumper = dmp.CommonDump()
    dumper.handle_arch_file(file_path)
    assert current_path != None, 'none'
    assert os.path.exists(output_dir), f'fail to run'
    files = os.listdir(output_dir)
    py_files = [x for x in files if x.endswith('.py')]
    assert len(
        py_files) > 0, f'seems no py file is success to decompile,{files}'
    shutil.rmtree(output_dir)


def test_arch_file_pycdc(res_type_arch: Tuple):
    configuration.progress_session_timeout = 120
    configuration.plugin_decompiler_enable_pycdc = True
    return start_arch_file(res_type_arch)


def test_arch_file_uncompyle6(res_type_arch: Tuple):
    configuration.progress_session_timeout = 120
    configuration.plugin_decompiler_enable_uncompyle6 = True
    return start_arch_file(res_type_arch)
