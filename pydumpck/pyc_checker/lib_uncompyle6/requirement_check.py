from ... import logger


def check(v_expected: str, v_current: str) -> bool:
    def get_ver_value(v):
        v = [int(x) for x in v.split('.')]
        return (v[0] << 24) + (v[1] << 12) + v[2]
    cur_value = get_ver_value(v_current)
    exp_value = get_ver_value(v_expected)
    result = exp_value <= cur_value
    return result, exp_value, cur_value


def check_version():
    import xdis.version
    v_expected = '6.0.4'
    v_current = xdis.version.__version__

    fit, exp, cur = check(v_expected, v_current)
    if not fit:
        logger.warning(
            f'require xdis version greater than {v_expected},current is {v_current}')
        if input('install package online? yes(*)/no(n)') == 'n':
            import sys
            sys.exit(-1)
        import pip
        pip.main(['install', '--upgrade', 'xdis'])
