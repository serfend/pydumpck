import argparse
from . import __version__
from .py_common_dump import CommonDump


def run():
    parser = argparse.ArgumentParser(description=__version__.__description__)
    parser.add_argument(
        'target_file',
        help="file to extract or decompiler,combine with -y for type select."
    )

    parser.add_argument(
        '-o',
        '--ouput',
        default='./output',
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
        help='thread count for running (default: %(default)s) cpu-count * 2.',
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
        '-y',
        '--type',
        default=None,
        type=str,
        dest='target_file_type',
        help='file-type of input file,can use pe,exe,elf,pyc,pyz (default: %(default)s : auto guess).',
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
    args = parser.parse_args()
    if not args.show_version == False:
        print(__version__.__version__)
        return
    try:
        dmp = CommonDump()
        raise SystemExit(dmp.main(**vars(args)))
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")


if __name__ == '__main__':
    run()
    # main('http_server.exe', './output')
