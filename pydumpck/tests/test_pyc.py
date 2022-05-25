import shutil
import os
from .common import res_type
import pydumpck.pyc_checker.lib_uncompyle6
import pydumpck.pyc_checker
import pydumpck.configuration
decompiler = pydumpck.pyc_checker.lib_uncompyle6.Decompiler()


def start_pyc_test():
    pydumpck.configuration.decompile_file = None
    pyc_path, t = res_type.get_res('pyc')
    target_file = f'{pyc_path}.py'
    content, err = pydumpck.pyc_checker.dump_pyc(
        pyc_file=pyc_path, target_file=target_file)
    is_notice = err and err[0:3] == '[*]'
    assert not is_notice, f'should not have notice:{err}'
    if not is_notice:
        assert err == None
        assert content != None
        assert isinstance(content, str)
        assert len(content) > 20
        assert os.path.exists(target_file)
        os.remove(target_file)


def test_pyc_decompiler_pycdc():
    pydumpck.configuration.plugin_decompiler_enable_pycdc = True
    return start_pyc_test()


def test_pyc_decompiler_pydecompyle6():
    pydumpck.configuration.plugin_decompiler_enable_uncompyle6 = True
    return start_pyc_test()
