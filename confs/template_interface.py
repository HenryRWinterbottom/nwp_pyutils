"""
Module
------

    template_interface.py

Description
-----------

    This module contains the base-class object for all file template
    rendering.

Classes
-------

    Template()

        This is the base-class object for all file template rendering.

Author(s)
---------

    Henry R. Winterbottom; 19 April 2023

History
-------

    2023-04-19: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# -----

from types import SimpleNamespace
from typing import Dict, Generic

from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.exceptions_interface import TemplateInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["Template"]

# ----

TMPL_ITEM_LIST = [
    "@[%s]",
    "[@%s]",
    "{@%s}",
    "{%%%s%%}",
    "{{%% %s %%}}",
    "<%s>",
    "{%% %s %%}",
    "{{ %s }}",
]

# ----


class Template:
    """
    Description
    -----------

    This is the base-class object for all file generic template
    rendering.

    """

    def __init__(self: Generic):
        """
        Description
        -----------

        Creates a new Template object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")

    def read_tmpl(self: Generic, tmpl_path: str) -> str:
        """
        Description
        -----------

        This method reads a template file path and returns a Python
        string containing the attributes collected from the file.

        Parameters
        ----------

        tmpl_path: ``str``

            A Python string defining the template file path.

        Returns
        -------

        tmpl_str_in: ``str``

            A Python string containing the attributes collected from
            the template file path.

        """

        # Read and return the attributes within the template file
        # path.
        with open(tmpl_path, "r", encoding="utf-8") as file:
            tmpl_str = file.read().split("\n")
        tmpl_str_in = " ".join([f"{item}\n" for item in tmpl_str])

        return tmpl_str_in

    @privatemethod
    def render_tmpl(
        self: Generic,
        tmpl_obj: SimpleNamespace,
        tmpl_str_in: str,
        fail_missing: bool,
        f90_bool: bool,
        warn: bool,
    ) -> str:
        """
        Description
        -----------

        This method renders a Python template string using the
        attributes specified in `tmpl_obj` upon entry and returns a
        Python string updated accordingly.

        Parameters
        ----------

        tmpl_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the template
            attributes.

        tmpl_str_in: ``str``

            A Python string containing template characters.

        fail_missing: ``bool``

            A Python boolean valued variable specifying whether to
            fail if a template string cannot be fully rendered.

        f90_bool: ``bool``

            A Python boolean valued variable specifying whether to
            transform boolean variables to a FORTRAN 90 format.

        warn: ``bool``

            A Python boolean valued variable specifying whether to
            create `Logger` warning messages for missing template
            variables.

        Returns
        -------

        tmpl_str_out: ``str``

            A Python string for which template characters have been
            rendered and otherwise identical to `tmpl_str_in`.

        Raises
        ------

        TemplateInterfaceError

            - raised if a template string has not been rendered and
              `fail_missing` is `True` upon entry.

        """

        # Initialize the output string.
        tmpl_str_out = tmpl_str_in

        # Replace any instances of templated strings with specified
        # attributes accordingly.
        for attr_key, attr_value in vars(tmpl_obj).items():
            for tmpl_item in TMPL_ITEM_LIST:
                try:
                    check_str = tmpl_item % attr_key
                    value = parser_interface.dict_key_value(
                        dict_in=vars(tmpl_obj), key=attr_key, force=True, no_split=True
                    )
                    # Update value accordingly.
                    if value is not None:
                        if f90_bool:
                            value = parser_interface.f90_bool(value=value)
                        attr_value = value
                        tmpl_str_out = tmpl_str_out.replace(check_str, str(attr_value))
                except TypeError:
                    pass

        # Define all characters that represent templated values.
        tmpl_char_list = set(
            list("".join([item.replace("%s", "") for item in TMPL_ITEM_LIST]))
        )
        tmpl_char_list = [item for item in tmpl_char_list if item != " "]

        # Check whether any templated strings remain; proceed
        # accordingly.
        tmpl_str_list = []
        for tmpl_str in tmpl_str_out.split("\n"):
            if any(item for item in tmpl_char_list if item in tmpl_str):
                tmpl_str_list.append(tmpl_str.strip())
        if warn:
            msg = (
                "The following template(s) was (were) not rendered: "
                f"{', '.join(tmpl_str_list)}."
            )
            if len(tmpl_str_list) > 0:
                if fail_missing:
                    msg = msg + " Aborting!!!"
                    raise TemplateInterfaceError(msg=msg)
                if not fail_missing:
                    self.logger.warn(msg=msg)

        return tmpl_str_out

    @staticmethod
    def tmpl_obj(attr_dict: Dict) -> SimpleNamespace:
        """
        Description
        -----------

        This method builds a Python object containing the attributes
        within the Python dictionary `attr_dict` upon entry.

        Parameters
        ----------

        attr_dict: ``Dict``

            A Python dictionary containing the attributes to be used
            for updating a specified template.

        Returns
        -------

        tmpl_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the template
            attributes provided by `attr_dict` upon entry and cast as
            an object.

        """

        # Collect the attributes within the Python dictionary provided
        # upon entry and builds a Python object.
        tmpl_obj = parser_interface.object_define()
        for attr in attr_dict.keys():
            value = parser_interface.dict_key_value(
                dict_in=attr_dict, key=attr, no_split=True
            )
            tmpl_obj = parser_interface.object_setattr(
                object_in=tmpl_obj, key=attr, value=value
            )

        return tmpl_obj

    def write_tmpl(
        self: SimpleNamespace,
        attr_dict: Dict,
        tmpl_path: str,
        template_path: str,
        fail_missing: bool = False,
        f90_bool: bool = False,
        warn: bool = True,
    ) -> None:
        """
        Description
        -----------

        This method collects attribute values, renders a string
        containing template attributes, and writes the updated
        template to a specified file path `tmpl_path`.

        Parameters
        ----------

        attr_dict: ``Dict``

            A Python dictionary containing the attributes to be used
            for updating a specified template.

        tmpl_path: ``str``

            A Python string specifying the rendered (e.g., output)
            file path.

        template_path: ``str``

            A Python string specifying the template file path to be
            rendered.

        Keywords
        --------

        fail_missing: ``bool``, optional

            A Python boolean valued variable specifying whether to
            fail if a template string cannot be fully rendered.

        f90_bool: ``bool``, optional

            A Python boolean valued variable specifying whether to
            transform boolean variables to a FORTRAN 90 format.

        warn: ``bool``, optional

            A Python boolean valued variable specifying whether to
            create `Logger` warning messages for missing template
            variables.

        """

        # Read, render, and write the template file.
        tmpl_obj = self.tmpl_obj(attr_dict=attr_dict)
        tmpl_str_in = self.read_tmpl(tmpl_path=template_path)
        tmpl_str_out = self.render_tmpl(
            tmpl_obj=tmpl_obj,
            tmpl_str_in=tmpl_str_in,
            fail_missing=fail_missing,
            f90_bool=f90_bool,
            warn=warn,
        )
        with open(tmpl_path, "w", encoding="utf-8") as file:
            for item in tmpl_str_out.split("\n"):
                file.write(f"{item.strip()}\n")
