import os
from .common import current_path
from .common.res_type import *
from pydumpck.py_common_dump import CommonDump


def test_current_path():
    assert current_path == os.path.dirname(__file__)


def test_check_file_type(res_type_all: Tuple):
    file_path, target_type, decompile_files = res_type_all
    reg_type = CommonDump().get_filetype(file_path)
    assert target_type == reg_type, f'dump file type unexpected:{target_type}|{reg_type} {file_path}'
