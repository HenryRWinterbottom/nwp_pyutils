"""
Module
------

    system_interface.py

Description
-----------

    This module contains functions to perform various system-level
    tasks.

Functions
---------

    __get_stack__()

        This function defines the calling application stack frame.

    app_path(app)

        This function invokes the POSIX UNIX command function to retrieve
        the path to the application specified upon entry.

    chown(path, user, group=None)

        This function changes the ownership credentials for the
        specified file path.

    get_app_path(app)

        This function collects the path for the specified application;
        if the path cannot be determined, NoneType is returned.

    get_hostname()

        This function returns the name assigned to the respective host
        platform.

    get_pid()

        This function returns the current process integer
        identification.

    sleep(seconds=0)

        This function allows specific calling applications to suspend
        execution for a specified number of seconds.

    task_exit()

        This function (gracefully) exits the respective application
        and returns a status code of 0 (i.e., success).

    user()

        This method returns the login name of the user.

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-with
# pylint: disable=redefined-outer-name
# pylint: disable=unused-variable

# ----

import getpass
import inspect
import os
import shutil
import socket
import subprocess
import sys
import time
from typing import List, Union

from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = [
    "app_path",
    "chown",
    "get_app_path",
    "get_hostname",
    "get_pid",
    "sleep",
    "task_exit",
    "user",
]

# ----

logger = Logger(caller_name=__name__)

# ----


def __get_stack__() -> List:
    """
    Description
    -----------

    This function defines the calling application stack frame.

    Returns
    -------

    stack: ``List``

        A Python list containing the calling application stack frame.

    """

    # Collect the calling application stack frame.
    stack = inspect.stack()

    return stack


# ----


def app_path(app: str) -> Union[str, None]:
    """
    Description
    -----------

    This function invokes the POSIX UNIX command function to retrieve
    the path to the application specified upon entry.

    Parameters
    ----------

    app: ``str``

        A Python string specifying the name of the application for
        which the path is to be determined.

    Returns
    -------

    path: ``Union[str, None]``

        A Python string specifying the path determined for the
        application name specified upon entry; if no path for the
        respective application name can be determined NoneType is
        returned.

    """

    # Query the run-time environment in order to collect the path for
    # the application name specified upon entry.
    cmd = ["command", "-V", app]
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    (out, err) = proc.communicate()

    # Collect the run-time environment path from the query for the
    # application name specified upon entry.
    if len(out) > 0:
        path = out.rstrip().decode("utf-8").split()[2]
    else:
        path = None

    return path


# ----


def chown(path: str, user: str, group: str = None) -> None:
    """
    Description
    -----------

    This function changes the ownership credentials for the specified
    file path.

    Parameters
    ----------

    path: ``str``

        A Python string specifying the file path for which to change
        the ownership credentials.

    user: ``str``

        A Python string specifying the host name for the user to be
        used for the file path ownership credentials.

    Keywords
    --------

    group: ``str``

        A Python string specifying the host group name to be user for
        the path owner credentials.

    """

    # Change the ownership credentials for the specified file path in
    # accordance with the parameter values provided upon entry.
    shutil.chown(path=path, user=user, group=group)


# ----


def get_app_path(app: str) -> Union[str, None]:
    """
    Description
    -----------

    This function collects the path for the specified application; if
    the path cannot be determined, NoneType is returned.

    Parameters
    ----------

    app: ``str``

        A Python string specifying the name of the application for
        which to return the respective path.

    Returns
    -------

    app_path: ``Union[str, None]``

        A Python string specifying the path to the application name
        provided upon entry; if the application path cannot be
        determined, this value is NoneType.

    """

    # Collect the application path.
    app_path = shutil.which(app)

    return app_path


# ----


def get_hostname() -> str:
    """
    Description
    -----------

    This function returns the name assigned to the respective host
    platform.

    Returns
    -------

    hostname: ``str``

        A Python string specifying the name assigned to the respective
        host platform.

    """

    # Collect the name assigned to the host.
    hostname = socket.gethostname()

    return hostname


# ----


def get_pid() -> int:
    """
    Description
    -----------

    This function returns the current process integer identification.

    Returns
    -------

    pid: ``int``

        A Python integer specifying the current process integer
        identification.

    """

    # Collect the current process integer identifier.
    pid = os.getpid()

    return pid


# ----


def sleep(seconds: int = 0) -> None:
    """
    Description
    -----------

    This function allows specific calling applications to suspend
    execution for a specified number of seconds.

    Keywords
    --------

    seconds: ``int``, optional

        A Python integer specifying the number of seconds for which to
        suspend execution.

    """

    # Suspend execution for the specified number of seconds.
    time.sleep(seconds)


# ----


def task_exit() -> None:
    """
    Description
    -----------

    This function (gracefully) exits the respective application and
    returns a status code of 0 (i.e., success).

    """

    # Define the calling application stack frame.
    stack = __get_stack__()

    # Define calling application attributes.
    [module, lineno] = (stack[2][1], stack[2][2])

    # Gracefully exit task.
    msg = f"Task exit called from file {module} line number {lineno}."
    logger.warn(msg=msg)
    sys.exit(0)


# ----


def user() -> str:
    """
    Description
    -----------

    This method returns the login name of the user.

    Returns
    -------

    username: ``str``

        A Python string specifying the login name of the user.

    """

    # Query the POSIX UNIX environment to determine the user invoking
    # this function.
    username = getpass.getuser()

    return username
