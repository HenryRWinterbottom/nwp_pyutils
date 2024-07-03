"""
Module
------

    enviro_interface.py

Description
-----------

    This module contains function and objects to parser run-time
    environments.

Functions
---------

    enviro_to_obj()

        This method collects the status of the environment upon entry
        and casts and returns the environment attributes as a Python
        SimpleNamespace object.

Author(s)
---------

    Henry R. Winterbottom; 21 March 2023

History
-------

    2023-03-21: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
from types import SimpleNamespace

from tools import parser_interface
from utils.exceptions_interface import EnviroInterfaceError

# ----

# Define all available module properties.
__all__ = ["enviro_to_obj"]

# ----


def enviro_to_obj() -> SimpleNamespace:
    """
    Description
    -----------

    This method collects the status of the environment upon entry and
    casts and returns the environment attributes as a Python
    SimpleNamespace object.

    Returns
    -------

    envobj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the environment
        attributes.

    Raises
    ------

    EnviroInterfaceError:

        - raised if an exception is encountered while parsing the
          environment and/or building the Python SimpleNamespace
          object.

    """

    # Collect the run-time argument environment and format
    # accordingly.
    envdict = parser_interface.dict_formatter(in_dict=dict(os.environ))

    # Build the SimpleNamespace object; proceed accordingly.
    envobj = parser_interface.object_define()
    for envvar in envdict:
        try:
            value = parser_interface.dict_key_value(
                dict_in=envdict, key=envvar, no_split=True
            )
            envobj = parser_interface.object_setattr(
                object_in=envobj, key=envvar, value=value
            )
        except Exception as errmsg:
            msg = (
                "Casting the runtime environment as a Python dictionary "
                f"failed with error {errmsg}. Aborting!!!"
            )
            raise EnviroInterfaceError(msg=msg) from errmsg

    return envobj
