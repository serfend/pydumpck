# modules here
from pydumpck.pyinstaller_dump import run
import sys
import os
src_path = os.path.realpath(__file__)
src_dir = os.path.dirname(src_path)
sys.path.append(src_dir)



if __name__ == '__main__':
    run()
