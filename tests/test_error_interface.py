#!/usr/bin/env python3

"""Script
------

    test_cli_interface.py

Description
-----------

    This script is the driver script for the `utils.cli_interface`
    module unit-tests.

Classes
-------

    TestErrorInterface()

        This the base-class object for all `error_interface` module
        unit-tests; it is a sub-class of TestCase.

Author(s)
---------

    Henry R. Winterbottom; 14 October 2023

"""

# ----

from unittest import TestCase
from utils.error_interface import Error

# ----


class TestErrorInterface(TestCase):
    """
    Description
    -----------

    This the base-class object for all `error_interface` module
    unit-tests; it is a sub-class of TestCase.

    """

    def test_error_instance(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `error_interface`
        `Error.__init__` method.

        """

        # Execute the unit-test.
        error = Error("An error occurred.")
        self.assertIsInstance(error, Error)

# ----


if __name__ == '__main__':
    unittest.main()
