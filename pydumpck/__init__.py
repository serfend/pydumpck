if bytes is str:
    raise Exception("""

=-=-=-=-=-=-=-=-=-=-=-=-=  WELCOME TO THE FUTURE!  =-=-=-=-=-=-=-=-=-=-=-=-=-=

pydumpck has transitioned to python 3. Due to the small size of the team behind it,
we can't reasonably maintain compatibility between both python 2 and python 3.
If you want to continue using the most recent version of pydumpck (you definitely
want that, trust us) you should upgrade to python 3. It's like getting your
vaccinations. It hurts a little bit initially but in the end it's worth it.

For more information, see here: https://github.com/serfend/pydumpck

Good luck!
""")
from sgtpyutils.logger import logger
import sys
import os
src_path = os.path.realpath(__file__)
src_dir = os.path.dirname(src_path)
sys.path.append(src_dir)
from pydumpck.pyinstaller_dump import run
