# ff-containers-sort

[![PyPi Package](https://img.shields.io/pypi/v/ff-containers-sort.svg)](https://pypi.org/project/ff-containers-sort/)

```bash
pip install ff-containers-sort
```

## Requirements

* Python 3.6+

## Overview

* sorts Firefox Containers

### Features

* alphabetical sorting of containers
* manual sorting mode
* safely updates containers.json after manual changes
* supports multiple Firefox profiles
* preserves Firefox private container objects
* creates backups of Firefox Container config prior to making changes
    * deletes backups older than 7 days
* tested on Linux, Windows & Mac

## Usage

```bash
ff-containers-sort [--no-sort] [--manual]
```

## Changelog

See [CHANGELOG.md](https://github.com/naamancampbell/ff-containers-sort/blob/main/CHANGELOG.md)

## License

See [LICENSE](https://github.com/naamancampbell/ff-containers-sort/blob/main/LICENSE)
