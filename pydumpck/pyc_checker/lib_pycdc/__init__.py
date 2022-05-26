import os
import shutil
import time
package_dir = os.path.dirname(os.path.realpath(__file__))
tool_pycdc: str = None


def use_pycdc():
    bin_path = f'{package_dir}{os.path.sep}'
    if os.name == 'nt':
        pycdc_file = f'{bin_path}pycdc.exe'
    else:
        pycdc_file = f'{bin_path}pycdc'
        if not os.path.exists(pycdc_file):
            print('[!] pycdc_file not exist , trying build it...')
            time.sleep(5)
            from . import build
            build_file = f'{build.build()}{os.path.sep}pycdc'
            shutil.move(build_file, pycdc_file)
            build.clear()

    if os.stat(pycdc_file).st_mode != 0o100777:
        print(f'[*] detect pycdc_file not executable,try auth:{pycdc_file}')
        os.chmod(pycdc_file, 0o100777)
    if not os.path.isfile(pycdc_file):
        raise Exception(f'[!] required binary file is not exist:{pycdc_file}')
    global tool_pycdc
    tool_pycdc = pycdc_file
