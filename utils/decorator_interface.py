"""
Module
------

    decorator_interface.py

Description
-----------

    This module contains various decorator functions available to all
    applications.

Functions
---------

    cli_decorator(description, schema_file, script_name):

        This function provides a decorator to be used as a generic
        interface for the command-line interface (CLI) functions.

    msg_except_handle(err_cls):

        This function provides a decorator to be used to raise
        specified exceptions

    privatemethod(member):

        This function provides a decorator to be used to desinated
        `private` methods within classes.

    script_wrapper(script_name):

        This function provides a decorator to be used for running a
        driver script (e.g., `main()`) .

Author(s)
---------

    Henry R. Winterbottom; 06 April 2023

History
-------

    2023-04-06: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=protected-access
# pylint: disable=unused-argument

# ----

import functools
import sys
import time
from collections.abc import Callable
from typing import Dict, Generic, Tuple

from tools.parser_interface import enviro_set

from utils import cli_interface
from utils.cli_interface import CLIParser
from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["cli_wrapper", "msg_except_handle", "privatemethod", "script_wrapper"]

# ----


def cli_wrapper(description: str, schema_file: str, script_name: str) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used as a generic
    interface for the command-line interface (CLI) functions.

    Parameters
    ----------

    description: ``str``

        A Python string specifying the helper function script description.

    schema_file: ``str``

        A Python string specifying the path to the YAML-formatted file
        containing the caller script CLI schema attributes.

    script_name: ``str``

        A Python string specifying the name of the caller script.

    Returns
    -------

    decorator: ``Callable``

        A Python decorator.

    """

    # Define the decorator.
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped_function(*args: Tuple, **kwargs: Dict):
            enviro_set(envvar="CLI_SCHEMA", value=schema_file)
            args_objs = CLIParser().build()
            parser = cli_interface.init(
                args_objs=args_objs, description=description, prog=script_name
            )
            options_obj = cli_interface.options(parser=parser)
            func(options_obj=options_obj, *args, **kwargs)

        return wrapped_function

    return decorator


# ----


def msg_except_handle(err_cls: Generic) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used to raise specified
    exceptions.

    Parameters
    ----------

    err_cls: ``Generic``

        A Python Generic object containing the Error subclass to be
        used for exception raises.

    Returns
    -------

    decorator: ``Callable``

        A Python decorator.

    """

    # Define the decorator.
    def decorator(func: Callable):
        def call_function(msg: str) -> None:
            raise err_cls(msg=msg)

        return call_function

    return decorator


# ----


def privatemethod(member: Generic) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used to designate
    `private` methods within classes.

    Parameters
    ----------

    member: ``Generic``

        A Python Generic object containing the respective base-class
        within which the respective private method exists.

    Returns
    -------

    decorator: ``Callable``

        A Python decorator.

    """

    # Define the decorator.
    @functools.wraps(member)
    def decorator(*args: Tuple, **kwargs: Dict):
        name = member.__name__
        caller = sys._getframe(1).f_code.co_name
        if (caller not in dir(args[0])) and (caller not in name):
            msg = f"{name} called by {caller} is a private method. Aborting!!!"
            raise Exception(msg)

        return member(*args, **kwargs)

    return decorator


# ----


def script_wrapper(script_name: str) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used for running a driver
    script (e.g., `main()`) .

    Parameters
    ----------

    script_name: ``str``

        A Python string specifying the name of the caller script.

    Returns
    -------

    decorator: ``Callable``

        A Python decorator.

    """

    # Define the decorator.
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapped_function(*args: Tuple, **kwargs: Dict):
            logger = Logger(caller_name=func.__name__)
            start_time = time.time()
            msg = f"Beginning application {script_name}."
            logger.status(msg=msg)
            func(*args, **kwargs)
            stop_time = time.time()
            msg = f"Completed application {script_name}."
            logger.status(msg=msg)
            total_time = stop_time - start_time
            msg = f"Total Elapsed Time: {total_time} seconds."
            logger.status(msg=msg)

        return wrapped_function

    return decorator
