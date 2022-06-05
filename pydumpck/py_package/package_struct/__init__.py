import os
from ... import configuration, pyc_checker, logger
from ...pyc_checker import extensions
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import time


class PackageStruct:
    struct_data: bytes
    encrypt_key_data: bytes
    encrypt_key_file: str

    handle_count: int = 0
    total_count: int = 0

    def __init__(self):
        self.packages = []
        self.pyz_files = []
        self.pyc_files = []
        self.handle_count = 0
        self.total_count = 0
        self.struct_data = None
        self.encrypt_key_data = None
        self.encrypt_key_file = None

        self.thread_count = configuration.thread_count or (
            multiprocessing.cpu_count() * 8)
        self.pool = ThreadPoolExecutor(max_workers=self.thread_count)

    @staticmethod
    def decompile_pyc(file: str):
        # TODO log error from dump
        try:
            t = configuration.thread_timeout
            code, err = pyc_checker.dump_pyc(file, file, t)
            if code:
                logger.info(
                    f'decompile bytecode on file:{file},length:{len(code)}')
            else:
                logger.warning(
                    f'fail to decompile bytecode on file:{file},with error:{err}')
        except Exception as e:
            logger.warning(
                f'Exception on decompile bytecode file:{file},with error:{err}')

    def callback_pyc_decompile(self, f: str):
        PackageStruct.decompile_pyc(f)
        self.handle_count += 1

    def progress_check_pyc_decompile(self):
        files = self.pyc_files
        self.pyc_files = []
        self.total_count = len(files)
        self.handle_count = 0
        if self.total_count == 0:
            return
        if configuration.DEBUG_TestPycDump:
            for f in files:
                self.callback_pyc_decompile(f)
        else:
            [self.pool.submit(self.callback_pyc_decompile, f) for f in files]
            return self.progress_waitter('decompile source file')

    def progress_waitter(self, description: str):
        start_time = time.time()
        time_out = configuration.progress_session_timeout
        while True:
            current_time = time.time()
            cost_time = current_time - start_time
            if cost_time > time_out:
                t = f'timeout:from {start_time} to {current_time}'
                c = f'cost:{cost_time},timeout={time_out}'
                raise Exception(f'{t}\n{c}\n')
            time.sleep(1)
            print('\r', f'[*] {description}:{self.handle_count}{os.path.sep}{self.total_count}',
                  end='', flush=True)
            if self.handle_count > 0 and self.handle_count >= self.total_count:
                break

    def progress_check_dumping_file(self):
        self.dump()
        return self.progress_waitter('dumping source file')

    def progress_check_extract_pyz(self):
        self.total_count = len(self.pyz_files)
        if self.total_count == 0:
            return
        self.handle_count = 0
        self.start_pyz_handle()
        return self.progress_waitter('dumping pyz files')

    def progress_check(self):
        logger.debug('\nexport pyc')
        self.progress_check_dumping_file()  # export pyc
        logger.debug('\ndecompile pyc')
        self.progress_check_pyc_decompile()  # decompile pyc
        logger.debug('\nextract pyz')
        self.progress_check_extract_pyz()  # extract pyz
        logger.debug('\ndecompile pyc for `extract pyz`')
        self.progress_check_pyc_decompile()  # decompile pyc for `extract pyz`
        logger.debug('\nprogress_check completed')
        pass

    def start_pyz_handle(self):
        if self.encrypt_key_file:
            src_file = extensions.get_pycdc_path(
                self.encrypt_key_file)
            if not os.path.exists(src_file):
                src_file = f'{extensions.get_uncompyle6_path(self.encrypt_key_file)}'
            if not os.path.exists(src_file):
                raise Exception(
                    'target file seems encrypted,but encrypt_key fetch fail.')
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
        package.parent = self
        self.packages.append(package)
        if package.name == 'struct':
            data = package.dump_raw_file()
            if data:
                self.struct_data = data[0:data.find(b'\xe3')]
                pyc_checker.default_pyc.file_header = self.struct_data
                logger.info(f'struct file found:{self.struct_data}')
        elif package.name == pyc_checker.pyimod00_crypto_key:
            self.encrypt_key_file = package.out_file
            logger.info(f'encrypt_file found:{self.encrypt_key_file}')

    def dump(self):
        packages = self.packages
        self.packages = []
        self.total_count = len(packages)
        self.handle_count = 0
        [self.pool.submit(self.handle_single, p) for p in packages]
