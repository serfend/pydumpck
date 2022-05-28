import struct
try:
    from io import BufferedReader
except:
    import BufferedReader
# Warning! pyc file should with its own header
# Here are for some situation when user just get a unexecutable pyc file
# will try to attach it
current_used_header:str = None


class PycHeader():
    @staticmethod
    def from_file(file: BufferedReader):
        file.seek(0)
        data = file.read(20)
        return PycHeader(data)

    def __init__(self, data: bytes):
        # before py3.7 its should be 12 , otherwise should be 16
        self.header_length, _ = self.get_e3(data)
        self.header_infos = struct.unpack('<HHIBBHI', data[0:self.header_length])
        pass

    def get_e3(self, data: bytes):
        pos = data.find(b'\xe3')
        return pos, data[pos:]


