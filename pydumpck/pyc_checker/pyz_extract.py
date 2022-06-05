from .. import logger
from typing import List
from io import BufferedReader
import os
import zlib
import sys
import struct
import marshal
import tinyaes
# imp is deprecated in Python3 in favour of importlib
if sys.version_info.major == 3:
    from importlib.util import MAGIC_NUMBER
    pyc_magic = MAGIC_NUMBER
else:
    import imp
    pyc_magic = imp.get_magic()


def decrypt_data(data: bytes, key: bytes):
    CRYPT_BLOCK_SIZE = 16
    iv = data[0:CRYPT_BLOCK_SIZE]
    cipher = tinyaes.AES(key, iv)
    return cipher.CTR_xcrypt_buffer(data[CRYPT_BLOCK_SIZE:])


def extract_pyz_from_arch(filename: str, key: bytes) -> List[str]:
    result = _extract(filename, key)
    return result


def _extract(name: str, key: bytes) -> List[str]:
    dirName = f'{name}_extract'
    # Create a directory for the contents of the pyz
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    with open(name, 'rb') as f:
        return _handle_file(f, dirName, key)


def _handle_file(f: BufferedReader, dirName: str, cipper_key: bytes):
    pyzMagic = f.read(4)
    assert pyzMagic == b'PYZ\0'  # Sanity Check

    pycHeader = f.read(4)  # Python magic value

    # Skip PYZ extraction if not running under the same python version
    if pyc_magic != pycHeader:
        logger.error('Warning: This script is running in a different Python version than the one used to build the executable.')

    (tocPosition, ) = struct.unpack('!i', f.read(4))
    f.seek(tocPosition, os.SEEK_SET)

    try:
        toc = marshal.load(f)
    except:
        logger.warning(
            'Unmarshalling FAILED. Cannot extract {0}. Extracting remaining files.'.format(dirName))
        return

    logger.info('Found {0} files in PYZ archive'.format(len(toc)))

    # From pyinstaller 3.1+ toc is a list of tuples
    if type(toc) == list:
        toc = dict(toc)

    def handle_single(key: str):
        (ispkg, pos, length) = toc[key]
        f.seek(pos, os.SEEK_SET)
        fileName = key
        # for Python > 3.3 some keys are bytes object some are str object
        if isinstance(fileName, bytes):
            fileName = fileName.decode('utf-8')
        # Prevent writing outside dirName
        fileName = fileName.replace('..', '__').replace('.', os.path.sep)

        if ispkg == 1:
            filePath = os.path.join(dirName, fileName, '__init__.pyc')
        else:
            filePath = os.path.join(dirName, fileName + '.pyc')

        fileDir = os.path.dirname(filePath)
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)

        def try_decompress(data: bytes):
            try:
                return (True, zlib.decompress(data))
            except:
                return (False, data)
        data = f.read(length)
        success, data = try_decompress(data)
        if not success:
            if cipper_key:
                # if fail to decompress , there might have a encrypt
                data_handled = decrypt_data(data, cipper_key)
                success, data = try_decompress(data_handled)
                if not success:
                    filePath = f'{filePath}.encrypted'
            else:
                filePath = f'{filePath}.unknown'
        open(filePath, 'wb').write(data)
        return filePath
    return [handle_single(key) for key in toc.keys()]

