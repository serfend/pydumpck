def print_banner():
    import base64
    import zlib
    import json
    data = b'eJztmstOwzAQRX8FdY2Qx4+xo1nDB8AS2LDPkv9nqooFphaPpM7Evar60LlSMpOkc2/dPB9e3p2jt+dQxItP6fM530GAAAECBAgQIEAYSDjc3ixMfu74mG+AgHqh43V4hPc/QhPlAgEB9UDkTnNA3+eHXwkmym6MOLg30IAI7g0EBPQNmXPvvxfUFKz5OZEWO/n5ySr+91nstJs1UZeSf2+7BuGifvqf0g61GTxJW14Nq569EIWik8Tz41eu38eYJU0V95NQCsJU86x8Eg411+1zEubKI7xuPzvhUnHS7WeW7GrOQoUkX9AVV7RAm4K5HHKpvfdLINYduGM+MXUo1i/GzMhe3yCH7bbLodqmDzOFeH0lz5LqRBDUsUOQVCeCRuLY4DpqZApPQblmkHgB+yRHKsTj+z5W51fpeg+7QmjobO7brp10adLMiDflrGgMgaE0AkOUFM8FBrIUGMK5wJAlJ+O/t/sjmwshPQTEic5xYvDdmBn+1+S4wzY2RiE+ZI0MGg18HRl0IOsnnZUVV6OOGjHy9lFCKyzhTJTQmVEKosQO+r2CsDAYXvNy2HX5C1fB9wKvovNh3d1MIac4wY044b/FCa+RhGJp3DwRz9w8wULshOuVj+bNE7r9TItvnmj90eFJR9DkJPMFQsjwAqKLiehiILHaRcbiCBDQNaJTgAiLA4SJZoDGQDD0nfsyDisQ0MbGrt+3pL/QXW3gRTkL139YNFYATDQDNAbqZewQIECAAAECBAgQ9iEcXj8Aln4rGA=='
    data = base64.b64decode(data)
    data = zlib.decompress(data)
    data = json.loads(data.decode('ascii'))
    [print(x) for x in data]
