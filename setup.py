#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os
import requests


long_description = 'a tool for decomplier exe,elf,pyz,pyc packed by python which is base on pycdc.sometimes its result not exactly right ,maybe could use uncompyle6 etc.'
if os.path.exists("requirements.txt"):
    install_requires = open("requirements.txt").read().split("\n")
else:
    install_requires = []

setup(
    name='pydumpck',
    version='1.0.1',
    keywords=('pydumpck', 'decomplier', 'pe', 'elf', 'pyc', 'pyz'),
    description='a pyfile decomplier base on pycdc for windows',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license='MIT Licence',
    url='https://github.com/serfend/pydumpck',
    author='serfend',
    author_email='serfend@foxmail.com',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pydump = main.__main__:main'
        ]
    }
)
