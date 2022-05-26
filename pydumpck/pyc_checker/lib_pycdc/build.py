from typing import Tuple
import zipfile
import os
import shutil
import time
import threading
import shutil
g_lock = threading.Lock()
build_cache: str = None


def get_self_path():
    return os.path.realpath(os.path.dirname(__file__))


def get_src_path():
    f = get_self_path()
    zip_file_path = os.path.join(f, 'src')
    zip_file = os.path.join(zip_file_path, 'pycdc.zip')
    src_path = os.path.join(zip_file_path, 'output')
    return zip_file, src_path


def __build():
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


def build() -> Tuple:
    '''
    compile binary and return path
        path:str binary
        is_building_without_cache:bool
    '''
    global build_cache
    global g_lock
    g_lock.acquire(True)
    if build_cache:
        g_lock.release()
        return build_cache, False
    export_file = f'{__build()}{os.path.sep}pycdc'
    build_cache = os.path.join(get_self_path(), '.cache')
    shutil.move(export_file, build_cache)
    g_lock.release()
    return build_cache, True


def clear():
    zip_file, src_path = get_src_path()
    shutil.rmtree(src_path)

def remove_cache():
    global build_cache
    global g_lock
    g_lock.acquire(True)
    build_cache = None
    g_lock.release()