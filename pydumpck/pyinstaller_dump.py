import __version__
import threading
import pyc_checker.pyz_extract
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import zipfile
import argparse
import os
import sys
import shutil
from PyInstaller.utils.cliutils.archive_viewer import get_archive, get_data, get_content, get_archive_content
from PyInstaller.utils.cliutils.archive_viewer import ZlibArchive
from PyInstaller.archive.readers import CArchiveReader, NotAnArchiveError
import pyc_checker
thread_count: int = 0
thread_timeout: int = 0
thread_output_directory: str = None


def handle_pyc_file(target_file: str):
    new_file = f'{thread_output_directory}{os.path.sep}{target_file}'
    if not os.path.exists(thread_output_directory):
        os.makedirs(thread_output_directory)
    shutil.copy(target_file, new_file)
    PackageStruct.decompile_pyc(None, new_file)


def handle_arch_file(target_file: str):
    arch = get_archive(target_file)
    extract_arch(arch, thread_output_directory)
    file_struct_pyc.progress_check()


action_dispatch = {
    'nofile': lambda target_file: print(target_file, "[-] is an invalid file name!", file=sys.stderr),
    'arch': handle_arch_file,
    'pyc': handle_pyc_file
}
action_map = {
    'exe': 'arch',
    'pe': 'arch',
    'elf': 'arch',
    'pyz': 'arch',
    'pyc': 'pyc',
}


def main(target_file: str, output_directory: str, thread: int = 0, timeout: int = 10, target_file_type: str = None, **args):
    global thread_count
    global thread_timeout
    global thread_output_directory
    thread_count = 1  # thread
    thread_timeout = timeout
    thread_output_directory = output_directory

    print(f'[+] input:{target_file},to:{output_directory}')
    if os.path.exists(output_directory):
        print(f'[+] removing output_directory')
        try:
            shutil.rmtree(output_directory)
        except:
            pass
    file_type = target_file_type or get_filetype(target_file)
    file_type = action_map[file_type] if file_type in action_map else None
    if not file_type in action_dispatch:
        result = f'unkonwn file-type:{file_type}'
    else:
        result = action_dispatch[file_type](target_file)
    print('[+] completed', result)


def get_filetype(filepath: str):
    if not os.path.isfile(filepath):
        return 'nofile'
    header_data: bytes = None
    with open(filepath, 'rb') as f:
        header_data = f.read(0x20)
    if header_data[0:2] == b'MZ':
        return 'exe'
    if header_data[0:4] == b'\x7fELF':
        return 'elf'
    if header_data.find(bytes.fromhex('e3' + '0' * 14)) > -1:
        return 'pyc'
    return 'TYPE_UNKNOWN'


def extract_arch(arch, current_directory: str):
    global file_struct_pyc
    if not os.path.exists(current_directory):
        os.makedirs(current_directory)
    children_package = arch.toc
    if isinstance(children_package, dict):
        children_package = filter(
            lambda x: not x.startswith('_'), list(children_package))
    else:
        children_package = children_package.data
    for package in children_package:
        p = PackageDescription(package, arch, current_directory)
        file_struct_pyc.add(p)


class PackageStruct:
    struct_data: bytes = None
    encrypt_key_data: bytes = None
    encrypt_key_file: str = None

    packages = []
    pyz_files = []
    pyc_files = []

    handle_count: int = 0
    total_count: int = 0

    def __init__(self):
        self.thread_count = thread_count or multiprocessing.cpu_count()
        self.pool = ThreadPoolExecutor(max_workers=self.thread_count)

    def decompile_pyc(self, file: str):
        # TODO log error from dump
        try:
            t = thread_timeout or 10
            code, err = pyc_checker.dump_pyc(file, f'{file}.py', t)
            if code:
                print('[+] decompiler bytecode', file, len(code))
            else:
                print('[!]fail to decompiler bytecode', file, err)
        except Exception as e:
            print('[!]Exception on decompiler bytecode', file, e)

    def callback_pyc_decompile(self, f: str):
        self.decompile_pyc(f)
        self.handle_count += 1

    def progress_check_pyc_decompile(self):
        files = self.pyc_files
        self.pyc_files = []
        self.total_count = len(files)
        self.handle_count = 0

        [self.pool.submit(self.callback_pyc_decompile, f) for f in files]
        return self.progress_waitter('decompile source file')

    def progress_waitter(self, description: str):
        while True:
            time.sleep(1)
            print('\r', f'[*] {description}:{self.handle_count}/{self.total_count}',
                  end='', flush=True)
            if self.handle_count > 0 and self.handle_count >= self.total_count:
                break

    def progress_check_dumping_file(self):
        file_struct_pyc.dump()
        return self.progress_waitter('dumping source file')

    def progress_check_extract_pyz(self):
        self.total_count = len(self.pyz_files)
        self.handle_count = 0
        self.start_pyz_handle()
        return self.progress_waitter('dumping pyz files')

    def progress_check(self):
        print('\nexport pyc')
        self.progress_check_dumping_file()  # export pyc
        print('\ndecompile pyc')
        self.progress_check_pyc_decompile()  # decompile pyc
        print('\nextract pyz')
        self.progress_check_extract_pyz()  # extract pyz
        print('\ndecompile pyc for `extract pyz`')
        self.progress_check_pyc_decompile()  # decompile pyc for `extract pyz`
        print('\nprogress_check completed')
        pass

    def start_pyz_handle(self):
        if self.encrypt_key_file:
            src_file = f'{self.encrypt_key_file}.py'
            with open(src_file, encoding='utf-8') as f:
                content = f.read()
                g_dict = {'key': None}
                exec(content, g_dict)
                key = g_dict['key']
                self.encrypt_key_data = key.encode('utf-8') if key else None
        for package in self.pyz_files:
            package.extract_pyz_arch()
            self.handle_count += 1

    def handle_single(self, package):
        package.extract()
        self.handle_count += 1

    def add(self, package):
        self.packages.append(package)
        if package.name == 'struct':
            data = package.dump_raw_file()
            if data:
                self.struct_data = data[0:data.find(b'\xe3')]
                pyc_checker.default_header = self.struct_data
                print('[+] struct file found', self.struct_data)
        elif package.name == 'pyimod00_crypto_key':
            self.encrypt_key_file = package.out_file
            print('[+] encrypt_file found', self.encrypt_key_file)

    def dump(self):
        packages = self.packages
        self.packages = []
        self.total_count = len(packages)
        self.handle_count = 0
        [self.pool.submit(self.handle_single, p) for p in packages]


file_struct_pyc: PackageStruct = PackageStruct()
global_lock = threading.Lock()


class PackageDescription:
    name: str = None
    type: str = None  # b(binary) x(extract) z(pyz) m(module)
    current_directory: str = None
    arch: CArchiveReader | ZlibArchive = None
    raw_file_init: bool = False

    def __init__(self, package: tuple | str, arch: CArchiveReader | ZlibArchive, current_directory: str):
        self.arch = arch
        self.current_directory = current_directory
        if isinstance(package, tuple):
            self.name = package[5]
            self.type = package[4]
        else:
            self.name = package
            self.type = 'm'

    def dump_to_file(self):
        self.dump_raw_file()
        if self.is_pyc:
            file_struct_pyc.pyc_files.append(self.out_file)

    def dump_raw_file(self):
        if self.raw_file_init:
            return None
        self.raw_file_init = True
        data = get_data(self.name, self.arch)
        directory = os.path.dirname(self.out_file)

        if not os.path.exists(directory):
            global global_lock  # TODO 优化高并发安全
            global_lock.acquire(True)
            if not os.path.exists(directory):
                os.makedirs(directory)
            global_lock.release()
        with open(self.out_file, 'wb') as f:
            f.write(data)
        return data

    def extract(self):
        self.dump_to_file()
        if self.type in 'z':
            global file_struct_pyc
            file_struct_pyc.pyz_files.append(self)
        if self.type in 'x':
            self.extract_common_arch()

    def extract_pyz_arch(self):
        global file_struct_pyc
        ext = pyc_checker.pyz_extract.extract_pyz_from_arch
        child_arch = ext(self.out_file, file_struct_pyc.encrypt_key_data)
        result = [file_struct_pyc.pyc_files.append(x) for x in child_arch]
        pass

    def extract_common_arch(self):
        try:
            lib = zipfile.ZipFile(self.out_file)
            lib.extractall(self.out_file_extract)
        except:
            pass

    @property
    def out_file(self):
        if self.is_pyc:
            p_name = f'{self.name}.pyc'
        else:
            p_name = self.name
        return f'{self.current_directory}/{p_name}'

    @property
    def is_pyc(self):
        return self.type in 'ms'

    @property
    def out_file_extract(self):
        return f'{self.out_file}_extract'


def run():
    parser = argparse.ArgumentParser(description=__version__.__description__)
    parser.add_argument(
        'target_file',
        help="file to extract or decompiler,combine with -y for type select."
    )

    parser.add_argument(
        '-o',
        '--ouput',
        default='./output',
        type=str,
        dest='output_directory',
        help='output archive file to (default: %(default)s).',
    )
    parser.add_argument(
        '-w',
        '--thread',
        default=0,
        type=int,
        dest='thread',
        help='thread count for running (default: %(default)s) cpu-count * 2.',
    )

    parser.add_argument(
        '-t',
        '--timeout',
        default=10,
        type=int,
        dest='timeout',
        help='timeout running single decompiler (default: %(default)s).',
    )

    parser.add_argument(
        '-y',
        '--type',
        default=None,
        type=str,
        dest='target_file_type',
        help='file-type of input file,can use pe,exe,elf,pyc,pyz (default: %(default)s : auto guess).',
    )
    parser.add_argument(
        '-v',
        '--version',
        default=False,
        nargs=argparse.OPTIONAL,
        type=bool,
        dest='show_version',
        help='show version of package',
    )
    args = parser.parse_args()
    if not args.show_version == False:
        print(__version__.__version__)
        return
    try:
        raise SystemExit(main(**vars(args)))
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")


if __name__ == '__main__':
    run()
    # main('http_server.exe', './output')
