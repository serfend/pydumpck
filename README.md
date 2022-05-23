

<p align="center">
    <a href="https://pypi.python.org/pypi/pydumpck/"><img alt="pypi version" src="https://img.shields.io/pypi/v/pydumpck.svg" /></a> 
    <a href="https://pypistats.org/packages/pydumpck"><img alt="pypi download" src="https://img.shields.io/pypi/dm/pydumpck.svg" /></a>
    <a href="https://github.com/serfend/pydumpck/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/serfend/pydumpck.svg?style=flat-square" /></a>
    <a href="https://github.com/serfend/pydumpck/releases"><img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/serfend/pydumpck/total.svg?style=flat-square&color=%2364ff82" /></a>
    <a href="https://github.com/serfend/pydumpck/commits"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/serfend/pydumpck.svg?style=flat-square" /></a>
</p>


![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)![Kali](https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white)![FreeBSD](https://img.shields.io/badge/-FreeBSD-%23870000?style=for-the-badge&logo=freebsd&logoColor=white)![Deepin](https://img.shields.io/badge/Deepin-007CFF?style=for-the-badge&logo=deepin&logoColor=white)![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)![Cent OS](https://img.shields.io/badge/cent%20os-002260?style=for-the-badge&logo=centos&logoColor=F0F0F0)

# What?

pydumpck is a tool for decompile exe,elf,pyz,pyc packed by python which is base on pycdc.sometimes its py-file result not exactly right ,maybe could use uncompyle6 etc.



## Install

```shell
pip install pydumpck
```



## Usage

```shell
usage: pydumpck [-h] [-o OUTPUT_DIRECTORY] [-w THREAD] [-t TIMEOUT] [-y TARGET_FILE_TYPE] target_file

positional arguments:
  target_file           PyInstaller archive to show content of

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIRECTORY, --ouput OUTPUT_DIRECTORY
                        output archive file to (default: ./output).
  -w THREAD, --thread THREAD
                        thread count for running (default: 0) cpu-count * 2.
  -t TIMEOUT, --timeout TIMEOUT
                        timeout running single decompiler (default: 10).
  -y TARGET_FILE_TYPE, --type TARGET_FILE_TYPE
                        file-type of input file,can use pe,exe,elf,pyc,pyz (default: None : auto guess).
```



## Example

```shell
pydumpck xxx.exe
pydumpck xxx.elf
pydumpck xxx.pyc
pydumpck xxx.pyz
pydumpck xxx.exe --output ./output --thread 8 --timeout 10
```



