"""
Module
------

    error_interface.py

Description
-----------

    This module loads the error package.

Classes
-------

    Error(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Exceptions.

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=raise-missing-from
# pylint: disable=unused-argument

# ----

from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["Error"]

# ----

logger = Logger(caller_name=__name__)

# ----


class Error(Exception):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Exceptions.

    Parameters
    ----------

    msg: ``str``

        A Python string containing a message to accompany the
        exception.

    """

    def __init__(self: Exception, msg: str) -> None:
        """
        Description
        -----------

        Creates a new Error object.

        """

        # Define the base-class attributes.
        logger.error(msg=msg)
        super().__init__()
