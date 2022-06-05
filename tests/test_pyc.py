import shutil
import os
from pydumpck import logger

from .common import res_type
import pydumpck.pyc_checker
import pydumpck.pyc_checker.extensions
import pydumpck.pyc_checker.lib_uncompyle6
import pydumpck.configuration
import pydumpck.py_common_dump
import pydumpck.utils.paths


def start_pyc_test():
    _ = pydumpck.py_common_dump.CommonDump().file_struct_pyc  # start dump global
    pydumpck.configuration.decompile_file = None
    pyc_path, t, _ = res_type.get_res('pyc')
    output_path = os.path.join(os.path.dirname(pyc_path), 'output')
    output_path = pydumpck.utils.paths.get_random_path(output_path)
    output_path = os.path.join(output_path, 'result')
    content, err = pydumpck.pyc_checker.dump_pyc(
        pyc_file=pyc_path, target_file=output_path)
    is_notice = err and not isinstance(err, Exception)
    logger.debug(f'complete with result err:{err},content:{content}')
    assert err == None or is_notice
    assert content != None
    assert isinstance(content, str)
    assert len(content) > 20
    p2 = pydumpck.pyc_checker.extensions.get_structed_path(output_path)
    assert os.path.exists(p2)
    os.remove(p2)
    return output_path


def test_pyc_decompiler_pycdc():
    pydumpck.configuration.plugin_decompiler_enable_pycdc = True
    path = start_pyc_test()
    p1 = pydumpck.pyc_checker.extensions.get_pycdc_path(path)
    assert os.path.exists(p1)
    shutil.rmtree(os.path.dirname(p1))


def test_pyc_decompiler_uncompyle6():
    pydumpck.configuration.plugin_decompiler_enable_uncompyle6 = True
    path = start_pyc_test()
    p1 = pydumpck.pyc_checker.extensions.get_uncompyle6_path(path)
    assert os.path.exists(p1)
    shutil.rmtree(os.path.dirname(p1))
