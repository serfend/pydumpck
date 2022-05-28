import os
current_path = os.path.dirname(__file__)
current_path = current_path[0:current_path.rfind(os.path.sep)]
sep = os.path.sep
resource_path = f'{current_path}{sep}resources'
resources = {
    'exe-encrypt': (f'{resource_path}{sep}exe{sep}exe-with-encrypt-demo.exe', 'exe', ['pyimod00_crypto_key', 'main', 'secret']),
    'exe-3.10': (f'{resource_path}{sep}exe-3.10{sep}http_server.exe', 'exe', ['main', 'server']),
    'elf': (f'{resource_path}{sep}elf{sep}elf-demo', 'elf', ['squid', 'squid_game']),
    'dis': (f'{resource_path}{sep}dis{sep}dis.dis', 'TYPE_UNKNOWN'),
    'pyc': f'{resource_path}{sep}pyc{sep}pyc-demo.pyc',
    'pyz': (f'{resource_path}{sep}pyz{sep}PYZ-00.pyz', 'pyz', ['squid_game']),
    'py': (f'{resource_path}{sep}py{sep}test_py.py', 'TYPE_UNKNOWN'),
    'TYPE_UNKNOWN': f'{resource_path}{sep}unknown{sep}test_unknown.py',
    'nofile': f'{resource_path}{sep}not_exist_path'
}
