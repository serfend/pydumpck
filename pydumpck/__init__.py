# modules here
import sys
import os
src_path = os.path.realpath(__file__)
src_dir = os.path.dirname(src_path)
sys.path.append(src_dir)

from .pyinstaller_dump import run as run_main
def run():
    run_main()


if __name__ == '__main__':
    run()
