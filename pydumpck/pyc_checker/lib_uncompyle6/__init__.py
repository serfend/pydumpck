try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO
from uncompyle6.parser import PythonParser, ParserError


def direct_error(self, instructions, index):
    raise ParserError(None, -1, self.debug['reduce'])


class Decompiler:
    def __init__(self):
        from .requirement_check import check_version
        check_version()
        from uncompyle6.main import decompile_file
        PythonParser.error = direct_error
        self.decompile_file = decompile_file

    def decompile(self, pyc_file: str, out_stream: StringIO = None) -> str:
        f = out_stream or StringIO()
        self.decompile_file(filename=pyc_file, outstream=f)
        f.seek(0)
        r = f.read()
        f.close()
        return r

    def decompile_content(self, pyc_file: str) -> str:
        return self.decompile(pyc_file)

    def decompile_to_file(self, pyc_file: str, target_file: str) -> str:
        with open(target_file, 'w+') as f:
            return self.decompile(pyc_file, f)


tool_uncompyle6: Decompiler = None


def use_uncompyle6():
    global tool_uncompyle6
    tool_uncompyle6 = Decompiler()
