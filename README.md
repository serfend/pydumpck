

<p align="center">
    <a href="https://github.com/serfend/pydumpck/"><img alt="pypi version" src="https://visitor-badge.glitch.me/badge?page_id=serfend/pydumpck&left_text=views" /></a> 
    <a href="https://pypi.python.org/pypi/pydumpck/"><img alt="pypi version" src="https://img.shields.io/pypi/v/pydumpck.svg" /></a> 
    <a href="https://pypistats.org/packages/pydumpck"><img alt="pypi download" src="https://img.shields.io/pypi/dm/pydumpck.svg" /></a>
    <a href="https://github.com/serfend/pydumpck/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/serfend/pydumpck.svg?style=flat-square" /></a>
    <a href="https://github.com/serfend/pydumpck/releases"><img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/serfend/pydumpck/total.svg?style=flat-square&color=%2364ff82" /></a>
    <a href="https://github.com/serfend/pydumpck/commits"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/serfend/pydumpck.svg?style=flat-square" /></a>
    <a href="https://github.com/serfend/pydumpck/actions/workflows/pytest.yml"><img alt="GitHub Workflow Status" src="https://github.com/serfend/pydumpck/actions/workflows/pytest.yml/badge.svg" /></a>
</p>




![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)![Kali](https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white)![FreeBSD](https://img.shields.io/badge/-FreeBSD-%23870000?style=for-the-badge&logo=freebsd&logoColor=white)![Deepin](https://img.shields.io/badge/Deepin-007CFF?style=for-the-badge&logo=deepin&logoColor=white)![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)![Cent OS](https://img.shields.io/badge/cent%20os-002260?style=for-the-badge&logo=centos&logoColor=F0F0F0)

# What?

pydumpck is a multi-threads tool for decompile exe,elf,pyz,pyc packed by python which is base on `pycdc` and `uncompyle6`.sometimes its py-file result not exactly right ,maybe could use uncompyle6.



## Install

```shell
pip install pydumpck
```



## Usage

```shell
usage: pydumpck [-h] [-o OUTPUT_DIRECTORY] [-w THREAD] [-t TIMEOUT] [--session-timeout TIMEOUT_SESSION]
                [-y TARGET_FILE_TYPE] [-d [DECOMPILE_FILE ...]] [--header [STRUCT_HEADERS ...]] [-v [SHOW_VERSION]]
                [-p [PLUGIN ...]]
                [target_file]

pydumpck is a multi-threads tool for decompile exe,elf,pyz,pyc packed by python which is base on pycdc and
uncompyle6.sometimes its py-file result not exactly right ,maybe could use uncompyle6.

positional arguments:
  target_file           file to extract or decompiler,combine with -y for type select.

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIRECTORY, --ouput OUTPUT_DIRECTORY
                        output archive file to (default: output_2938294).
  -w THREAD, --thread THREAD
                        thread count for running (default: 0) cpu-count * 8.
  -t TIMEOUT, --timeout TIMEOUT
                        timeout running single decompiler (default: 10).
  --session-timeout TIMEOUT_SESSION
                        timeout running total task (default: 10).
  -y TARGET_FILE_TYPE, --type TARGET_FILE_TYPE
                        file-type of input file,can use pe,exe,elf,pyc,pyz (default: None : auto guess).
  -d [DECOMPILE_FILE ...], --decompile_file [DECOMPILE_FILE ...]
                        only decompile referred file for quick complete (default: None).
  --header [STRUCT_HEADERS ...]
                        specify pyc header hex-string (default: None).if not set , pydumpck will use struct.pyc's
                        header(if possible) and default header.eg:6f0d0d0a 00000000 00000000 ffffffff
  -v [SHOW_VERSION], --version [SHOW_VERSION]
                        show version of package
  -p [PLUGIN ...], --plugin [PLUGIN ...]
                        enable decompiler plugins,split by space .example: `--plugin pycdc uncompyle6` (default:
                        ['pycdc']).available:pycdc,uncompyle6
```





## Quick Start

```shell
pydumpck xxx.exe
pydumpck xxx.elf
pydumpck xxx.pyc
pydumpck xxx.pyz
pydumpck xxx.exe --output ./output --thread 8 --timeout 10
```



## Example

- `-p/--plugin` specified which plugin to use for decompile (pycdc|uncompyle6)

`pydumpck xxx.exe -p uncompyle6`

`pydumpck xxx.exe -p pycdc uncompyle6`

- `-d/--decompile_file` specified which file(s) to decompile for a faster run

`pydumpck xxx.exe -d main` for only target `main.py`

`pydumpck xxx.exe -d main lib_base64 secert` for targets `main.py` and `lib_base64.py` and `secert.py`



## Demo

- pyc with header been tampered with
  - (Warning:gif with size 5MB)![pyc-fix_header-demo](https://raw.githubusercontent.com/serfend/res.image.reference/main/pyc-fix_header-demo.gif)



## Notice

> `pycdc` speed is more than 10 times faster than `uncompyle6` , and `uncompyle6` is not support for python that version above 3.8.
>
> however `pycdc` sometimes return a not precisely right result.
>
> in pydumpck , you can use `--plugin uncompyle6` for single-use or `--plugin pycdc uncompyle6` for both-use.



## Status

![Alt](https://repobeats.axiom.co/api/embed/013759c6315338178a2643de0bca01826fb39a14.svg "Repobeats analytics image")
