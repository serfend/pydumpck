import zipfile
import os
import shutil


def get_src_path():
    f = os.path.realpath(os.path.dirname(__file__))
    zip_file_path = os.path.join(f, 'src')
    zip_file = os.path.join(zip_file_path, 'pycdc.zip')
    src_path = os.path.join(zip_file_path, 'output')
    return zip_file, src_path


def build():
    # snapping
    previous_path = os.path.abspath(os.curdir)
    # extracting
    zip_file, src_path = get_src_path()
    zipfile.ZipFile(zip_file).extractall(src_path)
    # building
    os.chdir(os.path.abspath(src_path))
    os.system(f'cmake .')
    os.system(f'make')
    # clearing
    os.chdir(previous_path)
    return src_path


def clear():
    zip_file, src_path = get_src_path()
    shutil.rmtree(src_path)
