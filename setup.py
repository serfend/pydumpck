#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import sys

from setuptools import setup, find_packages
pck_name = 'pydumpck'
pck_dict = {}
pck_dict[pck_name] = pck_name
package_dir = os.path.dirname(os.path.realpath(__file__))
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


def remove_dist(target: str):
    if os.path.exists(target):
        shutil.rmtree(target)


def load_about():
    about = {}
    pck_dir = os.path.join(package_dir, pck_name)
    with open(os.path.join(pck_dir, '__version__.py'), 'r', encoding='utf-8') as f:
        exec(f.read(), about)
    return about


def clear_dist():
    remove_dist('./build')
    remove_dist('./pydumpck.egg-info')
    remove_dist(about['__public_path__'])


def load_requirements():
    if os.path.exists('requirements.txt'):
        install_requires = open('requirements.txt').read().splitlines()
    else:
        install_requires = []
    return install_requires


entry_points = {
    'console_scripts': [
        f'{pck_name} = {pck_name}:run',
    ],
}

about = load_about()
install_requires = load_requirements()
print('install_requires', install_requires)
clear_dist()
setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir=pck_dict,
    include_package_data=True,
    python_requires='>=3.7, <4',
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=about['__keywords__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(
        exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    platforms='any',
    install_requires=install_requires,
    entry_points=entry_points
)


def upload():
    pub = about['__public_path__']
    arr = ['twine', 'upload', f'{pub}/*', '--verbose']
    p = os.system(' '.join(arr))


# if any([x.find('dist') > -1 for x in sys.argv]):
#     upload()
