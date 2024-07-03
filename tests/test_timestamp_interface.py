#!/usr/bin/env python3

"""
Script
------

    test_timestamp_interface.py

Description
-----------

    This script is the driver script for the
    `utils.timestamp_interface` module unit-tests.

Classes
-------

    TestTimestampInterface()

        This the base-class object for all `timestamp_interface`
        module unit-tests; it is a sub-class of TestCase.

Author(s)
---------

    Henry R. Winterbottom; 14 October 2023

"""

# ----

# pylint: disable=undefined-variable

# ----

from unittest import TestCase

from utils.exceptions_interface import TimestampInterfaceError
from utils.timestamp_interface import check_frmt

# ----


class TestTimestampInterface(TestCase):
    """
    Description
    -----------

    This the base-class object for all `timestamp_interface` module
    unit-tests; it is a sub-class of TestCase.

    """

    def test_check_frmt_with_matching_formats(self: TestCase) -> None:
        """
        Description
        -----------

        This method checks whether the specified timestamp strings
        have matching formats.

        """

        # Execute the unit-test.
        datestr = "20231014120000"
        in_frmttyp = "%Y%m%d%H%M%S"
        out_frmttyp = "%Y%m%d%H%M%S"
        check_frmt(datestr, in_frmttyp, out_frmttyp)

    def test_check_frmt_with_different_formats(self: TestCase) -> None:
        """
        Description
        -----------

        This method checks whether the specified timestamp strings
        have different formats.

        """

        # Execute the unit-test.
        datestr = "2023-10-14T12:00:00Z"
        in_frmttyp = "%Y-%m-%dT%H:%M:%SZ"
        out_frmttyp = "%Y%m%d%H%M%S"
        with self.assertRaises(TimestampInterfaceError):
            check_frmt(datestr, in_frmttyp, out_frmttyp)

    def test_check_frmt_with_matching_default_formats(self: TestCase) -> None:
        """
        Description
        -----------

        This method checks whether the specified timestamp strings
        have matching default formats.

        """

        # Execute the unit-test.
        datestr = "20231014120000"
        check_frmt(datestr)

    def test_check_frmt_with_different_default_formats(self: TestCase) -> None:
        """
        Description
        -----------

        This method checks whether the specified timestamp strings
        have different default formats.

        """

        # Execute the unit-test.
        datestr = "2023-10-14T12:00:00Z"
        with self.assertRaises(ValueError):
            check_frmt(datestr)


# ----


if __name__ == "__main__":
    unittest.main()
