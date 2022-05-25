
import os
from ...configuration.res_lock import check_directory
from ...pyc_checker import pyz_extract
import zipfile
from PyInstaller.utils.cliutils.archive_viewer import get_archive, get_data, get_content, get_archive_content
from PyInstaller.archive.readers import CArchiveReader, NotAnArchiveError
from PyInstaller.utils.cliutils.archive_viewer import ZlibArchive


class PackageDescription:
    name: str = None
    type: str = None  # b(binary) x(extract) z(pyz) m(module)
    current_directory: str = None
    arch = None
    raw_file_init: bool = False
    exception: Exception = None  # save the error on dumping

    def __init__(self, package, arch, current_directory: str):
        self.arch = arch
        self.current_directory = current_directory
        self.parent = None
        if isinstance(package, tuple):
            self.name = package[5]
            self.type = package[4]
        else:
            self.name = package
            self.type = 'm'

    def dump_to_file(self):
        self.dump_raw_file()
        if self.is_pyc:
            # add pyc file to list , for latter decompile
            self.parent.pyc_files.append(self.out_file)

    def dump_raw_file(self):
        if self.raw_file_init:
            return None
        self.raw_file_init = True
        data = get_data(self.name, self.arch)
        directory = os.path.dirname(self.out_file)
        check_directory(directory)
        with open(self.out_file, 'wb') as f:
            f.write(data)
        return data

    def extract(self):
        try:
            self.dump_to_file()
            if self.type in 'z':
                self.parent.pyz_files.append(self)
            if self.type in 'x':
                self.extract_common_arch()
        except Exception as e:
            self.exception = e

    def extract_pyz_arch(self):
        ext = pyz_extract.extract_pyz_from_arch
        # use extractor to get all pyc files
        child_arch = ext(self.out_file, self.parent.encrypt_key_data)
        result = [self.parent.pyc_files.append(x) for x in child_arch]
        pass

    def extract_common_arch(self):
        try:
            lib = zipfile.ZipFile(self.out_file)
            lib.extractall(self.out_file_extract)
        except:
            pass

    @property
    def out_file(self):
        '''
        in arch , all module/resources are without extensions
        so we append pyc for module , directory for package
        '''
        if self.is_pyc:
            p_name = f'{self.name}.pyc'
        else:
            p_name = self.name
        return f'{self.current_directory}{os.path.sep}{p_name}'

    @property
    def is_pyc(self):
        return self.type in 'ms'

    @property
    def out_file_extract(self):
        return f'{self.out_file}_extract'
