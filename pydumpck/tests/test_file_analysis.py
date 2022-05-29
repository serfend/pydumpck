import os
from typing import Tuple
from .common import resources, current_path
import pydumpck.py_common_dump as dmp
import pydumpck.configuration as configuration
from .common.res_type import *
import shutil
import pydumpck.utils.paths
import pydumpck.utils.extensions
import pydumpck.pyc_checker.extensions


def start_arch_file(res_type_arch: Tuple):
    file_path, target_type, decompile_files = res_type_arch
    output_dir = f'{os.path.dirname(file_path)}{os.path.sep}{pydumpck.utils.paths.get_random_path("output")}'
    configuration.thread_output_directory = output_dir
    configuration.decompile_file = decompile_files
    dumper = dmp.CommonDump()
    dumper.handle_arch_file(file_path)
    assert current_path != None, 'none'
    assert os.path.exists(output_dir), f'fail to run'
    files = pydumpck.utils.extensions.flat(
        [files for root, dirs, files in os.walk(output_dir)])
    py_files = [x for x in files if x.endswith('.py')]
    py_files = [pydumpck.pyc_checker.extensions.get_filename(
        x) for x in py_files]
    py_files = pydumpck.utils.extensions.distinct(py_files)
    py_files = list(sorted(py_files))
    decompile_files = list(sorted(decompile_files))
    assert py_files == decompile_files, f'seems not equal decompile_files is success to decompile\ntarget files:{decompile_files},success:{py_files}'
    shutil.rmtree(output_dir)


def test_arch_file_pycdc(res_type_arch: Tuple):
    configuration.progress_session_timeout = 120
    configuration.plugin_decompiler_enable_pycdc = True
    return start_arch_file(res_type_arch)


def test_arch_file_uncompyle6(res_type_arch: Tuple):
    configuration.progress_session_timeout = 120
    configuration.plugin_decompiler_enable_uncompyle6 = True
    file_path, target_type, decompile_files = res_type_arch
    if '3.10' in file_path:
        return
    return start_arch_file(res_type_arch)
