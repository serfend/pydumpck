# from python.importlib._bootstrap_external


# use latest magic number of python release
from argparse import ArgumentError
from datetime import datetime
import struct
from ....utils.extensions import find
# before 3.7
# H     :version
# BB    :const \r\n
# I     :compile datetime
# I     :code description <co_size>
# ...   :code body
header_len_x3x07 = 0
# after 3.7
# H     :version
# BB    :const \r\n
# I     :sip_hash
# I     :compile datetime
# I     :code description <co_size>
# ...   :code body
header_len_x3x07_plus = 4
_versions = [
    ((3, 0x00a), 3439),
    ((3, 0x009), 3425),
    ((3, 0x008), 3413),
    ((3, 0x007), 3394),
    ((3, 0x006), 3379),
    ((3, 0x005), 3350),
    ((3, 0x004), 3310),
    ((3, 0x003), 3230),
    ((3, 0x002), 3180),
    ((3, 0x001), 3151),
    ((3, 0x000), 3131),
]


def get_timestamp(timestamp: datetime):
    if isinstance(timestamp, datetime):
        time_int = timestamp.timestamp()
    elif isinstance(timestamp, int):
        time_int = timestamp
    else:
        raise ArgumentError(message='invalid type of time')
    return struct.pack('<I', int(time_int))


def get_version(major: int = 3, minor: int = 0, build: int = None, timestamp: datetime = None):
    '''
    return 
        [
            0:Version:Tuple[major,minor],
            1:magic-number:int,
            2:demo-header:bytes
        ]
    '''
    if timestamp == None:
        timestamp = datetime.now()

    l = len(_versions)
    result = _versions[l-minor]

    header = bytearray()
    header += (struct.pack('<H', result[1]) + b'\r\n')
    if minor > 7:
        header += struct.pack('<I', 857944867)  # 23332333 unused mark
    # load datetime on now
    header += get_timestamp(timestamp)
    if minor > 3:
        header += (b'\xe9'*4)

    return [result[0], result[1], header]


version_count = len(_versions)
versions = [get_version(minor=(version_count-x)) for x in range(version_count)]
version_latest = versions[0]
version_py0304 = find(versions, lambda i, index: i[0][1] == 0x04)
pass
