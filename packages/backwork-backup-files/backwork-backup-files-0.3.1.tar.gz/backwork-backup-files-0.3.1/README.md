# backwork-backup-files [![Build Status](https://travis-ci.org/IBM/backwork-backup-files.svg?branch=master)](https://travis-ci.org/IBM/backwork-backup-files) [![PyPI version](https://badge.fury.io/py/backwork-backup-files.svg)](https://badge.fury.io/py/backwork-backup-files)

Add support for file backups on [`backwork`](https://github.com/IBM/backwork).

## Requirements
This plug-in is build on top of [`tar`](https://linux.die.net/man/1/tar).

## Installing
You can use `pip` to install this plug-in:
```sh
$ pip install backwork-backup-files
```

## Using
After installing the plug-in you will be able to use the `backup files` and `restore files` commands
on `backwork`:

#### backwork backup files

```sh
$ backwork backup files -h
usage: backwork backup files [-h] -f FILE

Back up one or more files. It uses `tar -cz` which gzips the output. You can
use any of the arguments supported by `tar`. Add a list of files and
directories you want backed up as the last thing in the line. Use `tar --help`
for more information.

optional arguments:
  -h, --help            show this help message and exit
  -o FILE, --output FILE  output gzipped file path
```

You can pass any option that you would normally use with `tar`:

```sh
$ backwork backup files -o foo.tgz --verbose /tmp /var/log
```

As shown in the `--help` message, there is one required arguments you
must use in your backup process.

`-o FILE` or `--output FILE` will save the output of `tar` into a
file.

#### backwork restore files

```sh
usage: backwork restore files [-h] input

Restore one or more files from a .tar.gz file. It uses `tar xvzf`. You can
use any of the arguments supported by `tar`. Use `tar --help` for more
information.

positional arguments:
  input       .tar.gz file to restore from

optional arguments:
  -h, --help  show this help message and exit
```

**Important:** There is a conflict with the `-h` argument since it is reserved
for the help/usage message. Use `--dereference` to follow symlinks.

## Building and Publishing

Travis will publish builds for you. To build, push a tag to the repo:

```
git tag -a v0.1.2 -m 'v0.1.2'
git push --tags
```
