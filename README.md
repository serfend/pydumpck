# pydumpck
> a tool for decomplier exe,elf,pyz,pyc packed by python which is base on pycdc.
>
> sometimes its result not exactly right ,maybe could use uncompyle6 etc.



<p align="center">
<a href="https://github.com/serfend/pydumpck/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/serfend/pydumpck.svg?style=flat-square" /></a>
<a href="https://github.com/serfend/pydumpck/releases"><img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/serfend/pydumpck/total.svg?style=flat-square&color=%2364ff82" /></a>
<a href="https://github.com/serfend/pydumpck/commits"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/serfend/pydumpck.svg?style=flat-square" /></a>
</p>

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

- demo

```shell
pydumpck xxx.exe
pydumpck xxx.elf
pydumpck xxx.pyc
pydumpck xxx.pyz
pydumpck xxx.exe --output ./output --thread 8 --timeout 10
```



