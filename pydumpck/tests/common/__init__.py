import os
current_path = os.path.dirname(__file__)
current_path = current_path[0:current_path.rfind(os.path.sep)]
resource_path = f'{current_path}/resources'
resources = {
    'exe': f'{resource_path}/exe/exe-with-encrypt-demo.exe',
    'elf': f'{resource_path}/elf/elf-demo',
    'dis': (f'{resource_path}/dis/dis.dis', 'TYPE_UNKNOWN'),
    'pyc': f'{resource_path}/pyc/pyc-demo.pyc',
    'pyz': f'{resource_path}/pyz/PYZ-00.pyz',
    'py': (f'{resource_path}/py/test_py.py', 'TYPE_UNKNOWN'),
    'TYPE_UNKNOWN': f'{resource_path}/unknown/test_unknown.py',
    'nofile': f'{resource_path}/not_exist_path'
}

