from ... import logger
def check(v_expected: str, v_current: str) -> bool:
    def get_ver_value(v):
        v = [int(x) for x in v.split('.')]
        return v[0] << 24 + v[1] << 12 + v[2]
    return get_ver_value(v_expected) <= get_ver_value(v_current)


def check_version():
    import xdis.version
    v_expected = '6.0.4'
    v_current = xdis.version.__version__

    if not check(v_expected, v_current):
        logger.warning(
            f'require xdis version greater than {v_expected},current is {v_current}')
        if input('install package online? yes(*)/no(n)') == 'n':
            import sys
            sys.exit(-1)
        import pip
        pip.main(['install', '--upgrade', 'xdis'])
