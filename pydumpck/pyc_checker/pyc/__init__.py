from ...configuration.res_lock import check_directory
from . import headers
import os


class PycHandler():
    def __init__(self, header_version: str = 'python_default_version'):
        h = None
        if header_version not in headers.__dict__:
            print(f'[!] not support python version {header_version}')
            self.show_all_supported_version()
            header_version = 'python_default_version'
        h = getattr(headers, header_version)
        self.used_header: bytes = bytes.fromhex(h)

    def show_all_supported_version(self):
        print('[*] all supported versions:')
        for i in headers.__dict__:
            print(i)

    def get_e3(self, data: bytes):
        pos = data.find(b'\xe3')
        # print(f'e3 pos:{pos}')
        return pos, data[pos:]

    def attach_header(self, data: bytes):
        pos, new_data = self.get_e3(data)
        same_header = data[0:pos] == self.used_header
        output_data = data if same_header else (self.used_header + new_data)
        return (same_header, output_data)

    def attach_pyc_struct(self, data: bytes, structed_pyc_file: str):
        same, data = self.attach_header(data)

        check_directory(os.path.dirname(structed_pyc_file))
        with open(structed_pyc_file, 'wb') as f:
            f.write(data)
        return same, data

default_pyc = PycHandler()