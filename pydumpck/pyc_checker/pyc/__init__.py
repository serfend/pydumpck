
import xdis.unmarshal
from typing import List, Tuple
from .. import logger
from ...configuration.res_lock import check_directory
from . import headers, magic_code
import os
import io


class PycHandler():
    def __init__(self, header: bytes = None):
        self.file_header: str = None  # file-header is from `struct` file which is credible
        self.header = header

    def check_marshal(self, data: bytes):
        '''
        use `xdis` to check any version of python suit for data
        return: (Tuple[int,int],int,int)
        '''
        pos, new_data = self.get_e3(data)
        fp: io.BytesIO = io.BytesIO(new_data)
        version_mode = magic_code.versions
        success_version_mode: Tuple = None
        for i in version_mode:
            try:
                code_obj = {}
                code = xdis.unmarshal._VersionIndependentUnmarshaller(
                    fp=fp,
                    magic_int=i[1],
                    bytes_for_s=True,
                    code_objects=code_obj)
                result = code.load()
                success_version_mode = i
                break
            except Exception as e:
                pass
            fp.seek(0)
        if success_version_mode:
            v, magic, demo_header = success_version_mode
            logger.info(f'find suitable python-version:{v},magic:{magic}')
            return bytes(demo_header)
        return None

    def get_e3(self, data: bytes):
        pos = data.find(b'\xe3')
        return pos, data[pos:]

    def attach_header(self, data: bytes):
        if self.file_header:
            h = self.file_header
        elif self.header:
            h = self.header
        else:
            h = self.check_marshal(data)
            if not h:
                raise Exception('[!] invalid pyc-struct data')
        pos, new_data = self.get_e3(data)
        same_header = data[0:pos] == h
        output_data = data if same_header else (h + new_data)
        return (same_header, output_data)

    def attach_pyc_struct(self, data: bytes, structed_pyc_file: str):
        same, data = self.attach_header(data)

        check_directory(os.path.dirname(structed_pyc_file))
        with open(structed_pyc_file, 'wb') as f:
            f.write(data)
        return same, data


default_pyc = PycHandler()
