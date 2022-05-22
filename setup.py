#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os
import requests


# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to': 'rst', 'from': 'markdown'},
                      files={'input_files[]': open(from_file, 'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


md_to_rst("README.md", "README.rst")


if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding="utf-8").read()
else:
    long_description = 'Add a fallback short description here'

if os.path.exists("requirements.txt"):
    install_requires = open("requirements.txt").read().split("\n")
else:
    install_requires = []

setup(
    name='pydump',
    version='1.0.0',
    keywords=('pydump', 'decomplier', 'pe', 'elf', 'pyc', 'pyz'),
    description='a pyfile decomplier base on pycdc for windows',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    long_description='a tool for decomplier exe,elf,pyz,pyc packed by python which is base on pycdc.sometimes its result not exactly right ,maybe could use uncompyle6 etc.',
    license='MIT Licence',
    url='https://github.com/serfend/pydump',
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
