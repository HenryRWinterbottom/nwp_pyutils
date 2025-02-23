"""
Module
------

    curl_interface.py

Description
-----------

    This module contains functions to create and collect internet
    (world-wide web; WWW) files using the respective platform curl
    application executable..

Functions
---------

    __check_curl_env_()

        This function checks whether the run-time environment contains
        the curl application executable; if not, a CurlInterfaceError
        exception will be raised; if so, the path to the curl
        executable will be defined and returned.

    get_webfile(url, path, ignore_missing=False)

        This function collects the specified URL path using the
        respective platform curl application executable.

    get_weblist(url, ext=None):

        This function collects a list of files beneath the specified
        URL.

Requirements
------------

- bs4; https://www.crummy.com/software/BeautifulSoup/

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-with

# ----

import os
import subprocess
from typing import List

import requests
from bs4 import BeautifulSoup
from tools import system_interface
from utils.exceptions_interface import CurlInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["get_webfile", "get_weblist"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __check_curl_env__() -> str:
    """
    Description
    -----------

    This function checks whether the run-time environment contains the
    curl application executable; if not, an CurlInterfaceError
    exception will be raised; if so, the path to the curl executable
    will be defined and returned.

    Returns
    -------

    curl_exec: ``str``

        A Python string specifying the path to the curl application
        executable.

    Raises
    ------

    CurlInterfaceError:

        - raised if the curl application executable path cannot be
          determined.

    """

    # Check the run-time environment in order to determine the curl
    # application executable path.
    curl_exec = system_interface.get_app_path(app="curl")
    if curl_exec is None:
        msg = (
            "The curl application executable could not be determined "
            "from the run-time environment. Aborting!!!"
        )
        raise CurlInterfaceError(msg=msg)

    return curl_exec


# ----


def get_webfile(
    url: str, path: str, local_filename: str = None, ignore_missing: bool = False
) -> None:
    """
    Description
    -----------

    This function collects the specified URL path using the respective
    platform curl application executable.

    Parameters
    ----------

    url: ``str``

        A Python string specifying the path to the internet
        (world-wide web; WWW) file to be retrieved.

    path: ``str``

        A Python string specifying the local path to which to write
        the retrieved file.

    Keywords
    --------

    local_filename: ``str``, optional

        A Python string specifying the basename path to which the
        collected URL path is to be written; the respective (renamed)
        URL will be written to the directory in which the application
        was launched.

    ignore_missing: ``bool``, optional

        A Python boolean valued variable specifying whether to ignore
        missing files (`True`) or raise a CurlInterfaceError exception
        for missing files (`False`).

    Raises
    ------

    CurlInterfaceError:

        - raised if an exception is raised related to a missing URL
          path is encountered.

    """

    # Establish the curl application executable path.
    curl_exec = __check_curl_env__()

    # Collect the internet-based file and proceed accordingly.
    msg = f"Collecting URL path {url}."
    logger.info(msg=msg)
    try:
        # Define the current working directory.
        cwd = os.getcwd()

        # Check whether to rename the download file; proceed
        # accordingly.
        if local_filename is None:
            # Define the standard output stream and the curl
            # application executable command line arguments.
            msg = f"Writing collected URL path {url} to local path {path}."
            stdout = subprocess.PIPE
            cmd = [f"{curl_exec}", "-C", "-", "-O", url]
        if local_filename is not None:
            # Open the output file and proceed accordingly.
            local_filepath = os.path.join(cwd, local_filename)
            msg = f"Writing collected URL path {url} and writing to path {local_filepath}."
            stdout = open(f"{local_filepath}", "wb")
            cmd = [f"{curl_exec}", "-o", local_filepath, url]

        # Collect the URL path(s).
        logger.info(msg=msg)
        proc = subprocess.Popen(cmd, stdout=stdout, stderr=subprocess.PIPE)
        proc.communicate()
        proc.wait()

        # Close the output file; proceed accordingly.
        try:
            stdout.close()
        except AttributeError:
            pass
        os.chdir(cwd)

    except Exception as errmsg:
        # Proceed accordingly for internet-based file paths that are
        # missing.
        if ignore_missing:
            pass
        if not ignore_missing:
            msg = (
                f"Collecting of internet path {url} failed with error {errmsg}. "
                "Aborting!!!"
            )
            raise CurlInterfaceError(msg=msg) from errmsg


# ----


def get_weblist(url: str, ext: str = None) -> List:
    """
    Description
    -----------

    This function collects a list of files beneath the specified URL.

    Parameters
    ----------

    url: ``str``

        A Python string specifying the path to the internet
        (world-wide web; WWW) file to be retrieved.

    Keywords
    --------

    ext: ``str``, optional

        A Python string specifying the web filename extension; if
        NoneType on entry the value defaults to to an empty string.

    Returns
    -------

    weblist: ``List``

        A Python list containing the files beneath the specified URL.

    Raises
    ------

    CurlInterfaceError:

        - raised if an Exception is encountered while attempting to
          compile a list of files beneath the specified URL.

    """

    # Collect a list of files beneath the specified URL path; proceed
    # accordingly.
    try:
        # Define the URL path and parse the retrieved file.
        webpage = requests.get(url=url, timeout=None).text
        soup = BeautifulSoup(webpage, "html.parser")

        # Compile a list of all URL paths.
        if ext is None:
            ext = str()
        webfiles = (
            url + "/" + node.get("href")
            for node in soup.find_all("a")
            if node.get("href").endswith(ext)
        )
        weblist = []
        for webfile in webfiles:
            weblist.append(webfile)
    except Exception as errmsg:
        msg = (
            f"Collection of files available at internet path {url} failed "
            f"with error {errmsg}. Aborting!!!"
        )
        raise CurlInterfaceError(msg=msg) from errmsg

    return weblist
