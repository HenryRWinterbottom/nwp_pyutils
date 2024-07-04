[![License](https://img.shields.io/badge/License-GPL-black)](https://github.com/HenryRWinterbottom/nwp_pyutils/blob/develop/LICENSE.md)
![Linux](https://img.shields.io/badge/Linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/Python-3.5|3.6|3.7-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-purple.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/nwp-pyutils/badge/?version=latest)](https://nwp-pyutils.readthedocs.io/en/latest/?badge=latest)
[![Coverage](https://codecov.io/gh/HenryRWinterbottom/nwp_pyutils/branch/develop/graph/badge.svg)](https://codecov.io/gh/HenryRWinterbottom/nwp_pyutils)

[![Build Tests](https://github.com/HenryRWinterbottom/nwp_pyutils/actions/workflows/buildtest.yaml/badge.svg)](https://github.com/HenryRWinterbottom/nwp_pyutils/actions/workflows/buildtest.yaml)
[![Unit Tests](https://github.com/HenryRWinterbottom/nwp_pyutils/actions/workflows/unittests.yaml/badge.svg)](https://github.com/HenryRWinterbottom/nwp_pyutils/actions/workflows/unittests.yaml)
[![Python Coding Standards](https://github.com/HenryRWinterbottom/nwp_pyutils/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryRWinterbottom/nwp_pyutils/actions/workflows/pycodestyle.yaml)


# Overview

This repository contains an application programming interface (API)
for common Python utilities used in various numerical weather prediction
(NWP) and data assimilation related applications.

- **Authors:** [Henry R. Winterbottom](mailto:hrwinterbottomwxdev@gmail.com)
- **Maintainers:** Henry R. Winterbottom
- **Copyright:** Henry R. Winterbottom

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, follow these steps:

~~~shell
user@host:$ git clone https://github.com/HenryRWinterbottom/nwp_pyutils
~~~

# Installing Package Dependencies

To install the Python packages required by `nwp_pyutils`, execute the
following commands:

~~~shell
user@host:$ cd /path/to/nwp_pyutils
user@host:$ pip install --upgrade pip
user@host:$ pip install -r requirements.txt
~~~

For more information on using pip and requirements.txt files, refer
[here](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

# Building and Installing

To install using Python setup tools, proceed as follows:

~~~shell
user@host:$ cd /path/to/nwp_pyutils
user@host:$ python setup.py build --user
user@host:$ python setup.py install --user
~~~

For additional information and options for building Python packages,
see [here](https://docs.python.org/3.5/distutils/setupscript.html).

# Docker Containers

Docker containers with `nwp_pyutils` dependencies can be obtained as
follows:

~~~shell
user@host:$ docker pull ghcr.io/henryrwinterbottom/ubuntu20.04.nwp_pyutils:latest
~~~

To run within the Docker container, use the following command:

~~~shell
user@host:$ docker run -it ghcr.io/henryrwinterbottom/ubuntu20.04.nwp_pyutils:latest
~~~

# Forking

If you wish to contribute modifications from your fork(s) to the main
repository, please first submit an issue. Use the following naming
conventions for your forks:

- `docs/user_fork_name`: Documentation additions or corrections.

- `feature/user_fork_name`: Additions, enhancements, or upgrades.

- `bug/user_fork_name`: Bug fixes not requiring immediate attention.

- `hotfix/user_fork_name`: Urgent bug fixes compromising application integrity.
