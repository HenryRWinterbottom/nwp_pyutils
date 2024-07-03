#!/usr/bin/env python3

"""
Script
------

    test_exceptions_interface.py

Description
-----------

    This script is the driver script for the
    `utils.exceptions_interface` module unit-tests.

Classes
-------

    TestExceptionsInterface()

        This is the base-class object for all `exceptions_interface`
        Error sub-class unit-tests; it is a sub-class of TestCase.

Functions
---------

    generate_error_class_tests(error_class)

        This is a wrapper function from which a unit-test will be
        executed for the respective Error class.

Author(s)
---------

    Henry R. Winterbottom; 14 October 2023

"""

# ----

# pylint: disable=redefined-outer-name
# pylint: disable=undefined-variable

# ----

from unittest import TestCase

from utils.error_interface import Error
from utils.exceptions_interface import (
    Boto3InterfaceError,
    CLIInterfaceError,
    ContainerInterfaceError,
    CurlInterfaceError,
    DateTimeInterfaceError,
    EnviroInterfaceError,
    GRIBInterfaceError,
    HashLibInterfaceError,
    Jinja2InterfaceError,
    JSONInterfaceError,
    NamelistInterfaceError,
    NetCDF4InterfaceError,
    NOAAHPSSInterfaceError,
    ParserInterfaceError,
    SchemaInterfaceError,
    SQLite3InterfaceError,
    SubprocessInterfaceError,
    TarFileInterfaceError,
    TCVitalsInterfaceError,
    TemplateInterfaceError,
    TimestampInterfaceError,
    URLInterfaceError,
    WgetInterfaceError,
    XArrayInterfaceError,
    XMLInterfaceError,
    YAMLInterfaceError,
)

# ----


def generate_error_class_tests(error_class) -> Error:
    """
    Description
    -----------

    This is a wrapper function from which a unit-test will be executed
    for the respective Error sub-class.

    """

    class TestExceptionsInterface(TestCase):
        """
        Description
        -----------

        This is the base-class object for all `exceptions_interface`
        Error sub-class unit-tests; it is a sub-class of TestCase.

        """

        def test_error_instance(self: TestCase) -> None:
            """
            Description
            -----------

            This is a wrapped function for the respective Error class
            unit-tests.

            """

            # Execute the unit-test.
            error = error_class("An error occurred.")
            self.assertIsInstance(error, Error)

    return TestExceptionsInterface


# ----


# Generate test classes for all error classes
error_classes = [
    Boto3InterfaceError,
    CLIInterfaceError,
    ContainerInterfaceError,
    CurlInterfaceError,
    DateTimeInterfaceError,
    EnviroInterfaceError,
    GRIBInterfaceError,
    HashLibInterfaceError,
    Jinja2InterfaceError,
    JSONInterfaceError,
    NamelistInterfaceError,
    NetCDF4InterfaceError,
    NOAAHPSSInterfaceError,
    ParserInterfaceError,
    SchemaInterfaceError,
    SQLite3InterfaceError,
    SubprocessInterfaceError,
    TarFileInterfaceError,
    TCVitalsInterfaceError,
    TemplateInterfaceError,
    TimestampInterfaceError,
    URLInterfaceError,
    WgetInterfaceError,
    XArrayInterfaceError,
    XMLInterfaceError,
    YAMLInterfaceError,
]

# For each error class execute the respective unit-test.
for error_class in error_classes:
    # Execute the respective Error sub-class unit-test.
    TestErrorClass = generate_error_class_tests(error_class)
    globals()[f"Test{error_class.__name__}"] = TestErrorClass

# ----

if __name__ == "__main__":
    unittest.main()
