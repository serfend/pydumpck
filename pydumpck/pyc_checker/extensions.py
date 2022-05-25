import os
extension_attachs = {
    'pycdc': '.cdc.py',
    'uncompyle6': '.up6.py',
    'structed': '.structed.pyc',
    'pyc': '.pyc'
}


def get_pycdc_path(raw_path: str) -> str:
    return f'{raw_path}{extension_attachs["pycdc"]}'


def get_uncompyle6_path(raw_path: str) -> str:
    return f'{raw_path}{extension_attachs["uncompyle6"]}'


def get_structed_path(raw_path: str) -> str:
    return f'{raw_path}{extension_attachs["structed"]}'


def get_filename(file_path: str) -> str:
    base = os.path.basename(file_path)
    for i in extension_attachs:
        v = extension_attachs[i]
        if base.endswith(v):
            base = base[0:(len(base)-len(v))]
    return base
