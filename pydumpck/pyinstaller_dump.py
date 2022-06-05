from . import logger
import argparse
from typing import List
import pydumpck.__version__ as __version__
from pydumpck.py_common_dump import CommonDump
import pydumpck.utils.paths
import time


def run():
    parser = argparse.ArgumentParser(description=__version__.__description__)
    parser.add_argument(
        'target_file',
        nargs=argparse.OPTIONAL,
        help="file to extract or decompiler,combine with -y for type select."
    )

    parser.add_argument(
        '-o',
        '--ouput',
        default=pydumpck.utils.paths.get_random_path('output'),
        type=str,
        dest='output_directory',
        help='output archive file to (default: %(default)s).',
    )
    parser.add_argument(
        '-w',
        '--thread',
        default=0,
        type=int,
        dest='thread',
        help='thread count for running (default: %(default)s) cpu-count * 8.',
    )

    parser.add_argument(
        '-t',
        '--timeout',
        default=10,
        type=int,
        dest='timeout',
        help='timeout running single decompiler (default: %(default)s).',
    )

    parser.add_argument(
        '--session-timeout',
        default=10,
        type=int,
        dest='timeout_session',
        help='timeout running total task (default: %(default)s).',
    )

    parser.add_argument(
        '-y',
        '--type',
        default=None,
        type=str,
        dest='target_file_type',
        help='file-type of input file,can use pe,exe,elf,pyc,pyz (default: %(default)s : auto guess).',
    )

    parser.add_argument(
        '-d',
        '--decompile_file',
        nargs=argparse.ZERO_OR_MORE,
        default=None,
        dest='decompile_file',
        help='only decompile referred file for quick complete (default: %(default)s).',
    )
    parser.add_argument(
        '--header',
        nargs=argparse.ZERO_OR_MORE,
        default=None,
        dest='struct_headers',
        help='specify pyc header hex-string (default: %(default)s).if not set , pydumpck will use struct.pyc\'s header(if possible) and default header.eg:6f0d0d0a 00000000 00000000 ffffffff',
    )
    
    parser.add_argument(
        '-v',
        '--version',
        default=False,
        nargs=argparse.OPTIONAL,
        type=bool,
        dest='show_version',
        help='show version of package',
    )

    parser.add_argument(
        '-p',
        '--plugin',
        default=['pycdc'],
        nargs=argparse.ZERO_OR_MORE,
        dest='plugin',
        help='enable decompiler plugins,split by space .example: `--plugin pycdc uncompyle6` (default: %(default)s).available:pycdc,uncompyle6',
    )
    args = parser.parse_args()
    if not args.show_version == False:
        v = __version__.__version__
        logger.debug(v)
        return v
    desc = parser.description + '\n' + '-' * 20
    content = f'pydumpck initilizing with {__version__.__version__}'
    logger.info(f'{desc}\n{content}')
    try:
        dmp = CommonDump()
        return dmp.main(**vars(args))
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")


if __name__ == '__main__':
    run()
