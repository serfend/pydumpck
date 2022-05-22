import os
import subprocess

default_header: bytes = bytes.fromhex('550D0D0A00000000FF7FFF61568C0000')
bin_path = './pyc_checker/bin/'
pycdc_file = f'{bin_path}pycdc.exe' if os.name == 'nt' else f'{bin_path}pycdc'

def get_e3(data: bytes):
    pos = data.find(b'\xe3')
    # print(f'e3 pos:{pos}')
    return data[pos:]


def attach_header(data: bytes):
    data = get_e3(data)
    return default_header + data


def remove_pycdc_banner(content: str):
    if not content:
        return None
    line_counter = 2
    while line_counter > 0:
        line_counter -= 1
        if content.startswith('#'):
            content = content[content.find('\n')+1:]
    return content


def use_pycdc(t_file: str, timeout: int = 10):
    try:
        p = subprocess.run([pycdc_file, t_file],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        content = p.stdout.decode('utf-8')
        err = p.stderr.decode('utf-8')
        return (remove_pycdc_banner(content), err)
    except Exception as e:
        return (None, e)


def dump(data: bytes, target_file: str, timeout: int = 10):
    data = attach_header(data)
    t_file = f'{target_file}.pyc'
    with open(t_file, 'wb') as f:
        f.write(data)
    content, err = use_pycdc(t_file, timeout)
    if not content:
        # print(f'[Warning]fail to handle {target_file}')
        return (None, err)
    os.remove(t_file)
    with open(target_file, 'w') as f:
        f.write(content)
    return (content, err)


def dump_pyc(pyc_file: str, target_file: str, timeout: int = 10):
    with open(pyc_file, 'rb') as f:
        data = f.read()
    return dump(data, target_file, timeout)
