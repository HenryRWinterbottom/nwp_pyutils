"""
Module
------

    github_interface.py

Description
-----------

Functions
---------

    __checkout__(git_obj, **kwargs)

        This function does a `git checkout` of the specified hash
        (i.e., artifact).

    __clobber__(git_obj)

        This function removes an existing local path for a GitHub URL
        clone.

    __clone__(git_obj)

        This function clones a specified GitHub URL to a specified
        local path.

    __schema__(git_obj)

        This function evaluates the attributes for the Python
        SimpleNamespace object `git_obj` upon entry and updates the
        respective Python SimpleNamespace object using the schema
        attributes.

    __status__(title, **kwargs)

        This function defines and returns the status bar object to be
        used for respective caller application/function.

    git_checkout(func)

        This function is a wrapper function for the respective GitHub
        checkout application.

    git_clone(func)

        This function is a wrapper function for the respective GitHub
        clone application.

    git_info(git_obj)

        This function defines a Python Simplenamespace object
        containing the respective GitHub package attributes.

Requirements
------------

- Gitpython; https://github.com/gitpython-developers/GitPython

- alive_progress: https://github.com/rsalmei/alive-progress

- pygithub; https://github.com/PyGithub/PyGitHub

Author(s)
---------

    Henry R. Winterbottom; 22 November 2023

History
-------

    2023-11-22: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=disallowed-name
# pylint: disable=not-callable
# pylint: disable=pointless-statement

# ----

import functools
import os
from types import SimpleNamespace
from typing import Callable, Dict, Tuple

from alive_progress import alive_bar
from alive_progress.core.progress import __AliveBarHandle
from confs.yaml_interface import YAML
from git import Repo
from tools import fileio_interface, parser_interface
from utils.exceptions_interface import GithubInterfaceError
from utils.logger_interface import Logger
from utils.schema_interface import build_schema, validate_schema

# ----

# Define all available module properties.
__all__ = ["git_checkout", "git_clone", "git_info"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __checkout__(git_obj: SimpleNamespace, **kwargs: Dict) -> None:
    """
    Description
    -----------

    This function does a `git checkout` of the specified hash (i.e.,
    artifact).

    Parameters
    ----------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        the respective GitHub package.

    Other Parameters
    ----------------

    kwargs: ``Dict``

        A Python dictionary of key and value pairs for the status bar
        object.

    """

    # Checkout the specified artifact for the respective GitHub
    # repository.
    if git_obj.hash is None:
        msg = (
            "No hash (i.e., artifact) has been defined for clone "
            f"{git_obj.path}; the default artifact will be used."
        )
        logger.warn(msg=msg)
    else:
        msg = f"Checking out artifact {git_obj.hash} from GitHub URL {git_obj.url}."
        logger.info(msg=msg)
        checkout_obj = Repo(git_obj.path).git.checkout(git_obj.hash)
        if git_obj.timing_bar:
            title = f"Checking out artifact {git_obj.hash}...\n\n"
            timing_bar = __status__(title=title, **kwargs)
            with timing_bar as bar:
                checkout_obj
                bar()
        else:
            checkout_obj


# ----


def __clobber__(git_obj: SimpleNamespace) -> None:
    """
    Description
    -----------

    This function removes an existing local path for a GitHub URL
    clone.

    Parameters
    ----------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        the respective GitHub package.

    """

    # Remove the existing local path for the respective GitHub URL
    # clone.
    if fileio_interface.fileexist(path=git_obj.path):
        msg = f"Local clone path {git_obj.path} exists and will be removed."
        logger.warn(msg=msg)


# ----


def __clone__(git_obj: SimpleNamespace) -> None:
    """
    Description
    -----------

    This function clones a specified GitHub URL to a specified local
    path.

    Parameters
    ----------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        the respective GitHub package.

    """

    # Clone the respective GitHub URL to the specified local path.
    Repo.clone_from(url=git_obj.url, to_path=git_obj.path, recursive=git_obj.recursive)


# ----


def __schema__(git_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Parameters
    ----------

    This function evaluates the attributes for the Python
    SimpleNamespace object `git_obj` upon entry and updates the
    respective Python SimpleNamespace object using the schema
    attributes.

    Parameters
    ----------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        the respective GitHub package.

    Returns
    -------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object update to contain the
        specified attributes as well as any schema assigned attributes
        for the respective GitHub package.

    Raises
    ------

    GithubInterfaceError:

        - raised if the schema evaluation for the respective GitHub
          package raise a TypeError exception; this is typically due
          to the `PYUTILS_ROOT` environment variable having not been
          defined in the run-time environment.

        - raised if the YAML-formatted schema file path does not
          exist.

    """

    # Check that the schema attributes are valid.
    git_dict = parser_interface.object_todict(object_in=git_obj)
    try:
        schema_path = os.path.join(
            parser_interface.enviro_get(envvar="PYUTILS_ROOT"),
            "sorc",
            "ioapps",
            "schema",
            "github.schema.yaml",
        )
    except TypeError as errmsg:
        msg = (
            "Defining the GitHub schema path failed with error "
            f"`{errmsg}`; please check that the environment variable "
            f"`PYUTILS_ROOT` is defined within the run-time environment. "
            "Aborting!!!"
        )
        raise GithubInterfaceError(msg=msg) from errmsg
    if not fileio_interface.fileexist(path=schema_path):
        msg = (
            f"The GitHub YAML-formatted schema file path {schema_path} "
            "does not exist. Aborting!!!"
        )
        raise GithubInterfaceError(msg=msg)
    msg = f"GitHub schema file is {schema_path}."
    logger.info(msg=msg)

    # Build the schema for the respective GitHub package.
    cls_schema = build_schema(schema_def_dict=YAML().read_yaml(yaml_file=schema_path))
    git_dict = validate_schema(cls_schema=cls_schema, cls_opts=git_dict)
    git_obj = parser_interface.dict_toobject(in_dict=git_dict)

    return git_obj


# ----


def __status__(title: str, **kwargs: Dict) -> __AliveBarHandle:
    """
    Description
    -----------

    This function defines and returns the status bar object to be used
    for respective caller application/function.

    Parameters
    ----------

    title: ``str``

        A Python string specifying the title for the status bar
        object.

    Other Parameters
    ----------------

    kwargs: ``Dict``

        A Python dictionary of key and value pairs for the status bar
        object.

    Returns
    -------

    status_bar: ``_AliveBarHandle``

        A Python _AliveBarHandle object containing the status bar.

    """

    # Define the status bar object.
    status_bar = alive_bar(0, title=title, **kwargs)

    return status_bar


# ----


def git_checkout(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for the respective GitHub
    checkout application.

    Parameters
    ----------

    func: ``Callable``

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: ``Callable``

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    def wrapped_function(*args: Tuple, **kwargs: Dict) -> Callable:
        """
        Description
        -----------

        This method runs the tasks for the respective GitHub package
        checkout application.

        Other Parameters
        ----------------

        args: Tuple

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: Dict

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Perform the respective GitHub package checkout application.
        git_obj = func(*args, **kwargs)
        __checkout__(git_obj=git_obj)

    return wrapped_function


# ----


def git_clone(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for the respective GitHub
    clone application.

    Parameters
    ----------

    func: ``Callable``

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: ``Callable``

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    def wrapped_function(*args: Tuple, **kwargs: Dict) -> Callable:
        """
        Description
        -----------

        This method runs the tasks for the respective GitHub package
        clone application.

        Other Parameters
        ----------------

        args: Tuple

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: Dict

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Perform the respective GitHub package clone application.
        git_obj = func(*args, **kwargs)
        msg = f"Cloning URL {git_obj.url} into file path {git_obj.path}."
        logger.info(msg=msg)
        __clobber__(git_obj=git_obj)
        fileio_interface.rmdir(git_obj.path)
        if git_obj.timing_bar:
            title = f"Cloning {git_obj.url}...\n\n"
            timing_bar = __status__(title=title)
            with timing_bar as bar:
                __clone__(git_obj=git_obj)
                bar()
        if not git_obj.timing_bar:
            __clone__(git_obj=git_obj)

    return wrapped_function


# ----


def git_info(git_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function defines a Python Simplenamespace object containing
    the respective GitHub package attributes.

    Parameters
    ----------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        the respective GitHub package.

    Returns
    -------

    git_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the validated
        schema attribute for the respective GitHub package clone.

    """

    # Collect/define the GitHub clone attributes.
    git_obj = __schema__(git_obj=git_obj)

    return git_obj
