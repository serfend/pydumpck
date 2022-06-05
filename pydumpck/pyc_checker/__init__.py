from .. import configuration, logger
from . import extensions, lib_pycdc, lib_uncompyle6
from .pyc import default_pyc, PycHandler
import os
import subprocess
pyimod00_crypto_key = 'pyimod00_crypto_key'


def remove_pycdc_banner(content: str):
    if not content:
        return None
    line_counter = 2
    while line_counter > 0:
        line_counter -= 1
        if content.startswith('#'):
            content = content[content.find('\n')+1:]
    return content


def remove_pyuncompyle6_banner(content: str):
    return content


def split_warning_error(content: str):
    lines = content.split('\n')
    other_error = []
    warning_error = []
    for i in lines:
        if i.startswith('Warning'):
            warning_error.append(i)
        else:
            other_error.append(i)
    err_other = '\n'.join(other_error)
    if not err_other:
        err_other = None
    err_warning = '\n'.join(warning_error)
    if not err_warning:
        err_warning = None
    return err_other, err_warning


def exec_pycdc(structed_pyc_file: str, target_file: str, timeout: int = 10):
    if not lib_pycdc.tool_pycdc:
        if configuration.plugin_decompiler_enable_pycdc:
            lib_pycdc.use_pycdc()
            return exec_pycdc(structed_pyc_file, target_file, timeout)
        return (None, 'pycdc not initilized')
    try:
        p = subprocess.run([lib_pycdc.tool_pycdc, structed_pyc_file],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        content = p.stdout.decode('utf-8')
        err, warning = split_warning_error(p.stderr.decode('utf-8'))
        if warning:
            logger.warning(
                f'\n{warning}\non exec_pycdc:{structed_pyc_file}')
        if not err:
            err = None
        result = (remove_pycdc_banner(content), err)
        if content:
            logger.info(
                f'decompile bytecode by pycdc success on file:{target_file},length:{len(result[0])}')
            with open(extensions.get_pycdc_path(target_file), 'wb') as f:
                f.write(result[0].encode('utf-8'))
        else:
            logger.warning(
                f'decompile bytecode by pycdc fail,file:{target_file},with error:{e}')
        return result
    except Exception as e:
        logger.warning(
            f'decompile bytecode by pycdc fail,file:{target_file},with error:{e}')
        return (None, e)


def exec_uncompyle6(structed_pyc_file: str, target_file: str, timeout: int = 10):
    if not lib_uncompyle6.tool_uncompyle6:
        if configuration.plugin_decompiler_enable_uncompyle6:
            lib_uncompyle6.use_uncompyle6()
            return exec_uncompyle6(structed_pyc_file, target_file, timeout)
        return (None, 'uncompyle6 not initilized')
    try:
        # TODO use asyncio,support timeout check
        r = lib_uncompyle6.tool_uncompyle6.decompile_to_file(
            pyc_file=structed_pyc_file,
            target_file=f'{target_file}.up6.py')
        r = remove_pyuncompyle6_banner(r)
        logger.info(
            f'decompile bytecode by uncompyle6 success file:{target_file},length:{len(r)}')
        return (r, None)
    except Exception as e:
        logger.error(
            f'decompile bytecode by uncompyle6 fail file:{target_file} ,with error :{e}')
        return (None, e)


def dump(data: bytes, target_file: str, structed_pyc_file: str, timeout: int = 10, use_attach_header: bool = True):
    if use_attach_header:
        same, data = default_pyc.attach_pyc_struct(data, structed_pyc_file)
    filename = extensions.get_filename(structed_pyc_file)
    if configuration.decompile_file != None and filename not in configuration.decompile_file and pyimod00_crypto_key != filename:
        return (None, f'not in decompile files:{filename}')
    content_cdc, err_cdc = exec_pycdc(structed_pyc_file, target_file, timeout)
    content_uncompyle6, err_uncompyle6 = exec_uncompyle6(
        structed_pyc_file, target_file, timeout)
    # TODO log error info
    content = content_cdc or content_uncompyle6
    err = err_cdc or err_uncompyle6
    err = Exception(
        err, f'fail when handling {target_file} -> {structed_pyc_file}') if isinstance(err, Exception) else err
    return (content, err)


def dump_pyc(pyc_file: str, target_file: str, timeout: int = 10, use_attach_header: bool = True):
    if use_attach_header:
        structed_pyc_file = extensions.get_structed_path(target_file)
        with open(pyc_file, 'rb') as f:
            data = f.read()
    else:
        structed_pyc_file = pyc_file
        data = None
    return dump(data, target_file, structed_pyc_file, timeout, use_attach_header)
