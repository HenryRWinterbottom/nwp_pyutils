#!/usr/bin/env python3

"""
Script
------

    test_decorator_interface.py

Description
-----------

    This script is the driver script for the
    `utils.decorator_interface` module unit-tests.

Classes
-------

    TestDecoratornterface()

        This the base-class object for all `decorator_interface`
        module unit-tests; it is a sub-class of TestCase.

Author(s)
---------

    Henry R. Winterbottom; 14 October 2023

"""

# ----

# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
# pylint: disable=undefined-variable
# pylint: disable=unused-argument

# ----

from typing import Callable, Generic
from unittest import TestCase

from utils.decorator_interface import (
    cli_wrapper,
    msg_except_handle,
    privatemethod,
    script_wrapper,
)

# ----


class TestDecoratorInterface(TestCase):
    """
    Description
    -----------

    This the base-class object for all `decorator_interface` module
    unit-tests; it is a sub-class of TestCase.

    """

    def test_cli_wrapper(self: TestCase):
        """
        Description
        -----------

        This method provides a unit-test for the `decorator_interface`
        `cli_wrapper` method.

        """

        # Execute the unit-test.
        @cli_wrapper("Description", "schema.yaml", "script_name")
        def sample_function(*args, **kwargs):
            """
            Description
            -----------

            This is a dummy function for the respective unit test(s).

            """

        self.assertIsInstance(sample_function, Callable)
        self.assertIsInstance(sample_function.__wrapped__, Callable)

    def test_msg_except_handle(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `decorator_interface`
        `msg_except_handle` method.

        """

        # Execute the unit-test.
        @msg_except_handle(Exception)
        def sample_function(msg):
            """
            Description
            -----------

            This is a dummy function for the respective unit test(s).

            """

        self.assertIsInstance(sample_function, Callable)

    def test_privatemethod(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `decorator_interface`
        `privatemethod` method.

        """

        # Execute the unit-test.
        class MyClass:
            """
            Description
            -----------

            This is a dummy object for the respective unit test(s).

            """

            @privatemethod
            def _private_method(self: Generic) -> None:
                """
                Description
                -----------

                This is a dummy method for the respective unit
                test(s).

                """

        obj = MyClass()
        with self.assertRaises(Exception):
            obj._private_method()

    def test_script_wrapper(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `decorator_interface`
        `script_wrapper` method.

        """

        # Execute the unit-test.
        @script_wrapper("script_name")
        def sample_function(*args, **kwargs):
            """
            Description
            -----------

            This is a dummy function for the respective unit test(s).

            """

        self.assertIsInstance(sample_function, Callable)
        self.assertIsInstance(sample_function.__wrapped__, Callable)


if __name__ == "__main__":
    unittest.main()
