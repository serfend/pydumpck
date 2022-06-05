from .. import logger
import math
import os
import shutil
import time
from typing import List
from .. import configuration, pyc_checker
from ..pyc_checker.pyc import PycHandler
from ..py_package import PackageStruct, PackageDescription
from PyInstaller.utils.cliutils.archive_viewer import get_archive, get_data, get_content, get_archive_content
from ..utils.banner import print_banner


class CommonDump():

    @property
    def file_struct_pyc(self):
        if not self._file_struct_pyc:
            self._file_struct_pyc = PackageStruct()
        return self._file_struct_pyc

    def __init__(self):
        self.total_handled_count = 0
        self._file_struct_pyc: PackageStruct = None
        self.action_dispatch = {
            'nofile': self.handle_nofile,
            'arch': self.handle_arch_file,
            'pyc': self.handle_pyc_file
        }
        self.action_map = {
            'exe': 'arch',
            'pe': 'arch',
            'elf': 'arch',
            'pyz': 'arch',
            'pyc': 'pyc',
        }

    def handle_nofile(self, target_file: str):
        logger.error(f'is an invalid file name! {target_file}')
        return -1

    @staticmethod
    def build_output_dir(clear=True):
        output_dir = configuration.thread_output_directory
        if clear and os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def handle_pyc_file(self, target_file: str):
        output_dir = self.build_output_dir()
        new_file = f'{output_dir}{os.path.sep}{target_file}'
        shutil.copy(target_file, new_file)
        PackageStruct.decompile_pyc(new_file)
        return f'pyc file handled:{new_file}'

    def handle_arch_file(self, target_file: str):
        output_dir = self.build_output_dir()
        arch = get_archive(target_file)
        self.extract_arch(arch, output_dir)
        self.file_struct_pyc.progress_check()
        return f'{self.total_handled_count} arch file(s) handled.'

    def load_plugins(self, plugin):
        self.any_invalid_plugin = False
        p_prefix = 'plugin_decompiler_enable_'

        def filter_plugin(p):
            n = f'{p_prefix}{p}'
            if n not in configuration.__dict__:
                self.any_invalid_plugin = True
                logger.error(f'no plugin named {p}')
                return None
            return [p, n]
        plugin = [filter_plugin(x) for x in plugin]
        plugin_paths = [x[1] for x in plugin if x]
        if self.any_invalid_plugin:
            keys = list(configuration.__dict__)
            all_valid_plugins = filter(lambda x: x.startswith(p_prefix), keys)
            all_valid_plugins = [x.replace(p_prefix, '')
                                 for x in all_valid_plugins]
            logger.debug(f'all valid plugins:{all_valid_plugins}')
            time.sleep(5)
        logger.debug(f'plugins loaded with {[x[0] for x in plugin if x]}')
        [setattr(configuration, x, True) for x in plugin_paths]

        if configuration.plugin_decompiler_enable_uncompyle6 and configuration.decompile_file == None:
            logger.error('attention! when use uncompyle6 , you should use --decompile_file specified which file to decompile for faster task.')
            time.sleep(3)

    def statistics_status(self, is_end: bool = False):
        if is_end:
            g = self.global_start_time
            cost = time.time() - g
            cost = math.ceil(cost*1e3)
            logger.info(f'completed,cost {cost}ms with result:{self.result}')
            return
        self.global_start_time = time.time()

    def main(self, target_file: str, output_directory: str, thread: int = 0, timeout: int = 10, target_file_type: str = None, session_timeout: int = 120, plugin: List = [], decompile_file: List = None, struct_headers: str = None, **args):
        self.statistics_status()
        print_banner()
        if struct_headers:
            pyc_header = bytes.fromhex(struct_headers.replace(' ', ''))
            pyc_checker.default_pyc = PycHandler(pyc_header)

        configuration.thread_count = thread  # thread
        configuration.thread_timeout = timeout
        configuration.thread_output_directory = output_directory
        configuration.progress_session_timeout = session_timeout
        configuration.decompile_file = dict(
            zip(decompile_file, [True for x in decompile_file])) if decompile_file else None
        self.load_plugins(plugin)
        if not target_file:
            logger.error('target_file is required')
            return
        os.chdir(os.path.dirname(target_file))
        logger.debug(f'target file input:{target_file}\nto:{output_directory}')

        if os.path.exists(output_directory):
            logger.info(f'removing output_directory')
            try:
                shutil.rmtree(output_directory)
            except:
                pass
        file_type = target_file_type or self.get_filetype(target_file)
        dispatch_to = self.action_map.get(file_type, None)
        if not dispatch_to in self.action_dispatch:
            self.result = f'unkonwn file-type:{file_type}->{dispatch_to}'
        else:
            logger.debug(f'start dump target file.')
            time.sleep(3)
            self.result = self.action_dispatch[dispatch_to](target_file)

        self.statistics_status(True)
        return self.result

    @staticmethod
    def get_filetype(filepath: str):
        if not isinstance(filepath, str) or not os.path.isfile(filepath):
            return 'nofile'
        header_data: bytes = None
        with open(filepath, 'rb') as f:
            header_data = f.read(0x20)
        if header_data[0:3] == b'MZ\x90':
            return 'exe'
        if header_data[0:4] == b'PYZ\x00':
            return 'pyz'
        if header_data[0:4] == b'\x7fELF':
            return 'elf'
        if header_data.find(bytes.fromhex('e3' + '0' * 14)) > -1:
            return 'pyc'
        return 'TYPE_UNKNOWN'

    def extract_arch(self, arch, current_directory: str):
        if not os.path.exists(current_directory):
            os.makedirs(current_directory)
        children_package = arch.toc
        if isinstance(children_package, dict):
            children_package = list(filter(
                lambda x: not x.startswith('_'), list(children_package)))
        else:
            children_package = children_package.data
        children_package = list(children_package)
        self.total_handled_count += len(children_package)
        for package in children_package:
            p = PackageDescription(package, arch, current_directory)
            self.file_struct_pyc.add(p)
