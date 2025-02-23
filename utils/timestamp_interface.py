"""
Module
------

    timestamp_interface.py

Description
-----------

    This module defines supported time-stamp string formats; all
    formats assume the POSIX UNIX convention.

Globals
-------

    GENERAL: str

        A timestamp format, assuming the POSIX convention, of
        `%Y-%m-%d_%H:%M:%S`.

    GLOBAL: str

        Global timestamp format; this is the format from which all
        others should be defined/determined; format is, assuming the
        POSIX convention, `%Y%m%d%H%M%S`.

    H: str

        A timestamp format, assuming the POSIX convention, of `%H`.

    INFO: str

        Information timestamp format; this format is typically used
        for informational purposes; format is, assuming the POSIX
        convention, `%H:%M:%S UTC %d %B %Y`.

    Y_m_dTHMSZ: str

        A timestamp format, assuming the POSIX convention, of
        `%Y-%m-%dT%H%M%SZ`.

    Ymd: str

        A timestamp format, assuming the POSIX convention, of `%Y%m%d`.

    YmdH: str

        A timestamp format, assuming the POSIX convention, of
        `%Y%m%d%H`.

    YmdTHM: str

        A timestamp format, assuming the POSIX convention, of
        `%Y%m%dT%H%M`.

    YmdTHMS: str

        A timestamp format, assuming the POSIX convention, of
        `%Y%m%dT%H%M%S`.

    YmdTHMZ: str

        A timestamp format, assuming the POSIX convention, of
        `%Y%m%dT%H%MZ`.

Functions
---------

    check_frmt(datestr, in_frmttyp = GLOBAL, out_frmttyp = GLOBAL)

        This function checks that the format for a provided timestamp
        matches the expected format.

Author(s)
---------

    Henry R. Winterbottom; 13 December 2022

History
-------

    2022-12-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=invalid-name

# ----

from tools import datetime_interface

from utils.exceptions_interface import TimestampInterfaceError

# ----

# Define all available module properties.
__all__ = [
    "GENERAL",
    "GLOBAL",
    "H",
    "INFO",
    "Y_m_dTHMSZ",
    "Ymd",
    "YmdH",
    "YmdTHM",
    "YmdTHMS",
    "YmdTHMZ",
    "check_frmt",
]

# ----

# Global timestamp format; this is the format from which all others
# should be defined/determined.
GENERAL = "%Y-%m-%d_%H:%M:%S"
GLOBAL = "%Y%m%d%H%M%S"
H = "%H"
INFO = "%H:%M:%S UTC %d %B %Y"
Y_m_dTHMSZ = "%Y-%m-%dT%H:%M:%SZ"
Ymd = "%Y%m%d"
YmdH = "%Y%m%d%H"
YmdTHM = "%Y%m%dT%H%M"
YmdTHMS = "%Y%m%dT%H%M%S"
YmdTHMZ = "%Y%m%dT%H%MZ"

# ----


def check_frmt(
    datestr: str, in_frmttyp: str = GLOBAL, out_frmttyp: str = GLOBAL
) -> None:
    """
    Description
    -----------

    This function checks that the format for a provided timestamp
    matches the expected format.

    Parameters
    ----------

    datestr: ``str``

        A Python string specifying the timestamp.

    Keywords
    --------

    in_frmttyp: ``str``, optional

        A Python string specifying the assumed format for the
        timestamp string parameter; this assumes the POSIX UNIX
        convention.

    out_frmttyp: ``str``, optional

        A Python string specifying the expected format for the
        timestamp string parameters; this assumes the POSIX UNIX
        convention.

    Raises
    ------

    TimestampInterfaceError:

        - raised if the provided timestamp string is not of the proper
          format.

    """

    # Define the timestamp string against which to compare the
    # parameter specified upon entry.
    check = datetime_interface.datestrupdate(
        datestr=datestr, in_frmttyp=in_frmttyp, out_frmttyp=out_frmttyp
    )
    if check != datestr:
        msg = (
            f"The timestamp string {datestr} does not match the format "
            f"{out_frmttyp}. Aborting!!!"
        )
        raise TimestampInterfaceError(msg=msg)
