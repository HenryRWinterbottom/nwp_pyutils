============================
UFS Python Utilities Toolbox
============================

Description
===========

A Python API toolbox for UFS-based applications.

- **confs**: Configuration-type file interfaces (e.g., JSON, LUA, YAML, XML, etc.).
- **execute**: Application execution interfaces (e.g., containers, executables, scripts, etc.).
- **ioapps**: File format read and write, and file staging and archiving interfaces.
- **tools**: Generic tools for all application interfaces.
- **utils**: Utility interfaces.

Developers
==========

* Henry R. Winterbottom - henry.winterbottom@noaa.gov

Cloning
=======

The ``ufs_pyutils`` repository can be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/HenryWinterbottom-NOAA/ufs_pyutils ./ufs_pyutils

Installing Package Dependencies
===============================

To install the Python packages upon which ``ufs_pyutils`` depends, follow these steps.

.. code-block:: bash

   user@host:$ /path/to/pip install --upgrade pip
   user@host:$ /path/to/pip install -r /path/to/ufs_pyutils/requirements.txt

Container Environments
======================

Docker container environments that support and within which the ``ufs_pyutils`` applications can be executed can be obtained and executed as follows.

.. code-block:: bash

   user@host:$ /path/to/docker run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest

.. toctree::
   :hidden:
   :maxdepth: 2

   confs
   execute
   ioapps
   tools
   utils
