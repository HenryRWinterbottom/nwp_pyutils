#!/usr/bin/env python3

"""
Script
------

    test_cli_interface.py

Description
-----------

    This script is the driver script for the `utils.cli_interface`
    module unit-tests.

Classes
-------

    TestCLIInterface()

        This the base-class object for all `cli_interface` module
        unit-tests; it is a sub-class of TestCase.

Author(s)
---------

    Henry R. Winterbottom; 14 October 2023

"""

# ----

# pylint: disable=undefined-variable

# ----

import os
from argparse import ArgumentParser
from collections import OrderedDict
from types import SimpleNamespace
from unittest import TestCase

from tools import parser_interface
from utils.cli_interface import (
    CLIParser,
    __checkschema__,
    __get_knownargs__,
    __get_otherargs__,
    init,
    options,
)

# ----


class TestCLIInterface(TestCase):
    """
    Description
    -----------

    This the base-class object for all `cli_interface` module
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self: TestCase):
        """
        Description
        -----------

        This method configures the base-class attributes for the
        respective unit-tests.

        """

        # Define the base-class attributes.
        self.schema_path = os.path.join(
            os.getcwd(), "tests", "test_files", "schema.yaml"
        )
        parser_interface.enviro_set(
            envvar="CLI_SCHEMA", value=self.schema_path)

    def test_init(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `cli_interface`
        `CLIParser.__init__` method.

        """

        # Execute the unit-test.
        cli_parser = CLIParser()
        self.assertIsInstance(cli_parser, CLIParser)
        self.assertIsInstance(cli_parser.cli_obj, SimpleNamespace)

    def test_build(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `cli_interface`
        `CLIParser.build` method.

        """

        # Execute the unit-test.
        cli_parser = CLIParser()
        args_objs = cli_parser.build()
        self.assertIsInstance(args_objs, tuple)
        for args_obj in args_objs:
            self.assertIsInstance(args_obj, SimpleNamespace)

    def test_checkschema(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `cli_interface`
        `CLIParser.checkschema` method.

        """

        # Execute the unit-test.
        options_obj = parser_interface.object_define()
        options_obj.variable1 = True
        options_obj.variable2 = 10.0
        options_obj.variable3 = 1
        schema_path = self.schema_path
        logger_method = "info"
        options_obj = __checkschema__(
            options_obj, schema_path, logger_method=logger_method
        )
        self.assertIsInstance(options_obj, OrderedDict)

    def test_get_knownargs(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `cli_interface`
        `__get_knownargs__` function.

        """

        # Execute the unit-test.
        parser = ArgumentParser()
        parser.add_argument("--arg1", type=int)
        parser.add_argument("--arg2", type=str)
        options_obj = __get_knownargs__(parser)
        self.assertIsInstance(options_obj, SimpleNamespace)

    def test_get_otherargs(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `cli_interface`
        `__get_otherargs__` function.

        """

        # Execute the unit-test.
        parser = ArgumentParser()
        parser.add_argument("--arg1", type=int)
        options_obj = SimpleNamespace(arg1=1)
        args = ["--arg2", "value"]
        parser.parse_known_intermixed_args(args)
        options_obj = __get_otherargs__(parser, options_obj)
        self.assertIsInstance(options_obj, SimpleNamespace)

    def test_init_argparser(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the ArgumentParser object
        instantiation.

        """

        # Execute the unit-test.
        args_objs = CLIParser().build()
        parser = init(args_objs=args_objs)
        self.assertIsInstance(parser, ArgumentParser)

    def test_options(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the `cli_interface`
        `options` function.

        """

        # Execute the unit-test.
        parser = ArgumentParser()
        parser.add_argument("--arg1", type=int)
        args = ["--arg1", "1", "--arg2", "value"]
        parser.parse_known_intermixed_args(args)
        options_obj = SimpleNamespace(arg1=1)
        options_obj = options(parser, validate_schema=False)
        self.assertIsInstance(options_obj, SimpleNamespace)


# ----


if __name__ == "__main__":
    unittest.main()
