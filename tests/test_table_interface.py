#!/usr/bin/env python3

"""
Script
------

    test_table_interface.py

Description
-----------

    This script is the driver script for the `utils.table_interface`
    module unit-tests.

Classes
-------

    TestTableInterface()

        This the base-class object for all `table_interface` module
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- tabulate; https://github.com/gregbanks/python-tabulate

Author(s)
---------

    Henry R. Winterbottom; 14 October 2023

"""

# ----

import unittest
from types import SimpleNamespace
from unittest import TestCase

from utils.table_interface import (
    __buildtbl__,
    __chkschema__,
    __getncols__,
    compose,
    init_table,
)

# ----


class TestTableInterface(TestCase):
    """
    Description
    -----------

    This the base-class object for all `table_interface` module
    unit-tests; it is a sub-class of TestCase.

    """

    def test_buildtbl(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `table_interface`
        `__buildtbl__` function.

        """

        # Execute the unit-test.
        table_obj = SimpleNamespace(
            table=[["A", "B", "C"], [1, 2, 3]],
            header=["Header1", "Header2", "Header3"],
            tablefmt="grid",
            numalign=["center", "right", "left"],
            colalign=["center", "center", "center"],
            disable_numparse=False,
        )
        table = __buildtbl__(table_obj)
        self.assertIsInstance(table, str)

    def test_chkschema(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `table_interface`
        `__chkschema__` function.

        """

        # Execute the unit-test.
        table_obj = SimpleNamespace(
            table=[["A", "B", "C"], [1, 2, 3]],
            header=["Header1", "Header2", "Header3"],
        )
        updated_table_obj = __chkschema__(table_obj)
        self.assertIsInstance(updated_table_obj, SimpleNamespace)
        self.assertEqual(updated_table_obj.tablefmt, "outline")
        self.assertEqual(updated_table_obj.numalign, ["center", "center", "center"])
        self.assertEqual(updated_table_obj.colalign, ["center", "center", "center"])
        self.assertFalse(updated_table_obj.disable_numparse)

    def test_getncols(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `table_interface`
        `__getncols__` function.

        """

        # Execute the unit-test.
        table_obj = SimpleNamespace(
            table=[["A", "B", "C"], [1, 2, 3]],
        )
        ncols = __getncols__(table_obj)
        self.assertEqual(ncols, 3)

    def test_compose(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `table_interface`
        `compose` function.

        """

        # Execute the unit-test.
        table_obj = SimpleNamespace(
            table=[["A", "B", "C"], [1, 2, 3]],
            header=["Header1", "Header2", "Header3"],
            tablefmt="grid",
            numalign=["center", "right", "left"],
            colalign=["center", "center", "center"],
            disable_numparse=False,
        )
        table = compose(table_obj)
        self.assertIsInstance(table, str)

    def test_init_table(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `table_interface`
        `init_table` function.

        """

        # Execute the unit-test.
        table_obj = init_table()
        self.assertIsInstance(table_obj, SimpleNamespace)
        self.assertEqual(table_obj.header, [])
        self.assertEqual(table_obj.table, [])


# ----


if __name__ == "__main__":
    unittest.main()
