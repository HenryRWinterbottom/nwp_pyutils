"""
Module
------

    yaml_interface.py

Description
-----------

    This module contains classes and methods to parse YAML-formatted
    template files and create an external file containing the user
    specified values.

Classes
-------

    YAML()

        This is the base-class object for YAML-formatted template file
        updates and the creation of a YAML-formatted file based on the
        template and the user-specified template variable key and
        value pairs.

    YAMLLoader()

        This is the base-class object for all YAML file parsing
        interfaces; it is a sub-class of SafeLoader.

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=too-many-ancestors
# pylint: disable=too-many-arguments

# ----

import os
import re
import sys
from types import SimpleNamespace
from typing import Any, Dict, Generic, List, Union

import yaml
from tools import fileio_interface, parser_interface
from utils.exceptions_interface import YAMLInterfaceError
from utils.logger_interface import Logger
from yaml import FullLoader, SafeLoader, ScalarNode

# ----

# Define all available module properties.
__all__ = ["YAML"]

# ----


class YAML:
    """
    Description
    -----------

    This is the base-class object for YAML-formatted template file
    updates and the creation of a YAML-formatted file based on the
    template and the user-specified template variable key and value
    pairs.

    """

    def __init__(self: Generic):
        """
        Description
        -----------

        Creates a new YAMLTemplate object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")

    def yaml_obj(self: Generic, attr_dict: Dict) -> SimpleNamespace:
        """
        Description
        -----------

        This method parses a Python dictionary containing attributes
        collected from a YAML-formatted file and returned as a Python
        object.

        Parameters
        ----------

        attr_dict: ``Dict``

            A Python dictionary containing the attributes collected
            from a YAML-formatted file.

        Returns
        -------

        yaml_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            collected from the Python dictionary provided upon entry.

        """

        # Collect the attributes within the Python dictionary provided
        # upon entry and build a Python object.
        (attr_list, yaml_obj) = ([], parser_interface.object_define())
        for attr in attr_dict.keys():
            attr_list.append(attr)
            value = parser_interface.dict_key_value(
                dict_in=attr_dict, key=attr, no_split=True
            )
            yaml_obj = parser_interface.object_setattr(
                object_in=yaml_obj, key=attr, value=value
            )

        return yaml_obj

    def check_yaml(self: Generic, attr_value: str) -> bool:
        """
        Description
        -----------

        This method checks whether the specified value for the
        `attr_value` parameter is a YAML-formatted file.

        Parameters
        ----------

        attr_value: ``str``

            A Python string containing an attribute value to be check
            for YAML-formatting.

        Returns
        -------

        check: ``bool``

            A Python boolean valued variable specifying whether the
            attribute value is a YAML-formatted file.

        """

        # Check that the file is a YAML-formatted file; proceed
        # accordingly.
        try:
            YAMLLoader(attr_value)
            check = True
        except AttributeError:
            check = False

        return check

    def concat_yaml(
        self: Generic,
        yaml_file_list: List,
        yaml_file_out: str,
        fail_nonvalid: bool = True,
        ignore_missing: bool = False,
    ) -> None:
        """
        Description
        -----------

        This method reads a list of YAML-formatted files and
        concatenates the contents into a single YAML-formatted file.

        Parameters
        ----------

        yaml_file_list: ``List``

            A Python list of YAML-formatted files.

        yaml_file_out: ``str``

            A Python string specifying the path to the YAML-formatted
            file containing the attributes collected from the
            respective YAML-formatted file list provided upon entry.

        Keywords
        --------

        fail_nonvalid: ``bool``, optional

            A Python boolean valued variable specifying whether to
            raise a YAMLInterfaceError exception if a YAML file path
            for concatenation is not a valid YAML-formatted file.

        ignore_missing: ``bool``, optional

            A Python boolean valued variable specifying whether to
            raise a YAMLInterfaceError exception if a YAML file path
            does not exist.

        Raises
        ------

        YAMLInterfaceError:

            - raised if a specified file is not a YAML-formatted
              and/or valid YAML file; invoked only if the respective
              specified file exists.

            - raised if a specified file path does not exist.

        """

        # Read the contents of the respective YAML-formatted files and
        # aggregate the values into a composite Python dictionary.
        yaml_dict_concat = {}
        for yaml_file in yaml_file_list:
            # Check that the respective YAML file path exists; proceed
            # accordingly.
            exist = fileio_interface.fileexist(path=yaml_file)
            if exist:
                try:
                    # Check that the respective file is a valid
                    # YAML-formatted file; proceed accordingly.
                    # yaml_dict.update(self.read_yaml(yaml_file=yaml_file))
                    yaml_dict = self.read_yaml(yaml_file=yaml_file)
                    try:
                        yaml_dict_concat.update(
                            dict(
                                parser_interface.dict_merge(
                                    dict1=yaml_dict_concat, dict2=yaml_dict
                                )
                            )
                        )
                    except Exception:
                        pass
                except ValueError as errmsg:
                    if fail_nonvalid:
                        msg = f"{yaml_file} is not a valid YAML file. Aborting!!!"
                        raise YAMLInterfaceError(msg=msg) from errmsg
                    if not fail_nonvalid:
                        msg = (
                            f"{yaml_file} is not a valid YAML file and will not "
                            "be processed."
                        )
                        self.logger.warn(msg=msg)
            if not exist:
                if ignore_missing:
                    msg = (
                        f"The file path {yaml_file} does not exist and "
                        "will not be processed."
                    )
                    self.logger.warn(msg=msg)
                if not ignore_missing:
                    msg = f"The file path {yaml_file} does not exist. " "Aborting!!!"
                    raise YAMLInterfaceError(msg=msg)

        # Write the resulting composite Python dictionary to
        # YAML-formatted file to contain the concatenated attributes.
        self.write_yaml(yaml_file=yaml_file_out, in_dict=yaml_dict_concat)

    def dict_to_yaml(
        self: Generic,
        yaml_dict: Dict,
        default_flow_style: bool = False,
        indent: int = 4,
        level: str = None,
        nspace: int = 0,
    ) -> None:
        """
        Description
        -----------

        This method writes the contents of the Python diction provided
        upon entry to a YAML-format in accordance with the keyword
        arguments specified upon entry.

        Parameters
        ----------

        yaml_dict: ``Dict``

            A Python dictionary containing the attributes to be
            written to a YAML-format.

        Keywords
        --------

        default_flow_style: ``bool``, optional

            A Python boolean valued variable; if `True` upon entry, the
            contents of the Python dictionary will not be serialized
            when written to YAML-format; if `False` upon the entry, the
            contents of the Python dictionary will be serialized in
            block style.

        indent: ``int``, optional

            A Python integer specifying the indent with for nest
            YAML-formatted blocks.

        level: ``str``, optional

            A Python string specifying the logger level to accompany
            the contents of the YAML-formatted Python dictionary; if
            NoneType upon entry, the contents will be written to
            standard out; otherwise the specified (and supported)
            level of the Logger object (see
            utils/logger_interface.py).

        nspace: ``int``, optional

            A Python integer specifying the total number of spaces to
            be used when the Logger object level is used; this is only
            implemented with the Logger interface is invoked.

        """

        # Dump the contents of the Python dictionary and define a
        # local object.
        yaml_dump = yaml.dump(
            yaml_dict, default_flow_style=default_flow_style, indent=indent
        )

        # Dump the contents of the Python dictionary to a YAML-format
        # in accordance with the parameters collected upon entry.
        if level is None:
            sys.stdout.write(yaml_dump)
        if level is not None:
            # Dump the contents of the Python dictionary using the
            # imported Logger object.
            logger = parser_interface.object_getattr(
                object_in=Logger(), key=level, force=True
            )
            msg = nspace * "\n" + yaml_dump
            logger(msg=msg)

    def read_concat_yaml(
        self: Generic, yaml_file: str, return_obj: bool = False
    ) -> Union[Dict, SimpleNamespace]:
        """
        Description
        -----------

        This method ingests a YAML Ain't Markup Language (e.g., YAML)
        formatted file and returns a Python dictionary containing the
        concatenated attributes of the file; this method is useful for
        parsing YAML-formatted files with embedded YAML-formatted file
        directives (e.g., the YAML-formatted file contains paths to
        external YAML-formatted files to also be parsed).

        Parameters
        ----------

        yaml_file: ``str``

            A Python string containing the full-path to the
            YAML-formatted file to be parsed.

        Keywords
        --------

        return_obj: ``bool``, optional

            A Python boolean valued variable specifying whether to
            return a Python SimpleNamespace object containing the
            YAML-formatted file contents; in this instance a Python
            dictionary will be defined using the contents of the
            YAML-formatted file and then the Python SimpleNamespace
            object will be constructed; if `True`, `yaml_obj` is
            returned instead of `yaml_dict`.

        Returns
        -------

        ``Union[Dict, SimpleNamespace]`` as follows.

        yaml_dict: ``Dict``

            A Python dictionary containing all attributes ingested
            from the YAML-formatted file; returned if return_obj is
            False upon entry.

        yaml_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing all attributes
            injested from the YAML-formatted file; returned if
            return_obj is True upon entry.

        """

        # Define the YAML library loader type.
        YAMLLoader.add_implicit_resolver("!ENV", YAMLLoader.envvar_matcher, None)
        YAMLLoader.add_constructor("!ENV", YAMLLoader.envvar_constructor)

        # Open and read the contents of the specified YAML-formatted
        # file path.
        with open(yaml_file, "r", encoding="utf-8") as stream:
            try:
                yaml_full_dict = yaml.load(stream, Loader=YAMLLoader)
            except yaml.composer.ComposerError:
                yaml_full_dict = yaml.load_all(stream, FullLoader)

        # For each attribute within the parsed YAML-formatted file,
        # determine whether a given file is a YAML-formatted file and
        # whether the respective YAML-formatted file exists; proceed
        # acccordingly.
        yaml_dict_concat = {}
        for attr_key in yaml_full_dict:
            # Collect the attribute corresponding to the respective
            # attribute; proceed accordingly.
            attr_value = parser_interface.dict_key_value(
                dict_in=yaml_full_dict, key=attr_key, no_split=True
            )
            is_yaml = self.check_yaml(attr_value=attr_value)

            # If the respective attribute value is a YAML-formatted
            # file, check that it exists and proceed accordingly.
            if is_yaml:
                exist = fileio_interface.fileexist(path=attr_value)
                if exist:
                    yaml_dict = self.read_yaml(yaml_file=attr_value)
                    yaml_dict_concat.update(
                        dict(
                            parser_interface.dict_merge(
                                dict1=yaml_dict_concat, dict2=yaml_dict
                            )
                        )
                    )
                if not exist:
                    yaml_dict_concat[attr_key] = attr_value
            if not is_yaml:
                yaml_dict_concat[attr_key] = attr_value

        # Define the Python data type to be returned; proceed
        # accordingly.
        if return_obj:
            yaml_return = self.yaml_obj(attr_dict=yaml_dict_concat)
        if not return_obj:
            yaml_return = yaml_dict_concat

        return yaml_return

    def read_yaml(
        self: Generic, yaml_file: str, return_obj: bool = False
    ) -> Union[Dict, SimpleNamespace]:
        """
        Description
        -----------

        This method ingests a YAML Ain't Markup Language (e.g., YAML)
        formatted file and returns a Python dictionary containing all
        attributes of the file.

        Parameters
        ----------

        yaml_file: ``str``

            A Python string containing the full-path to the YAML file
            to be parsed.

        Keywords
        --------

        return_obj: ``bool``, optional

            A Python boolean valued variable specifying whether to
            return a Python SimpleNamespace object containing the
            YAML-formatted file contents; in this instance a Python
            dictionary will be defined using the contents of the
            YAML-formatted file and then the Python SimpleNamespace
            object will be constructed; if `True`, `yaml_obj` is
            returned instead of `yaml_dict`.

        Returns
        -------

        ``Union[Dict, SimpleNamespace]`` as follows.

        yaml_dict: ``Dict``

            A Python dictionary containing all attributes ingested
            from the YAML-formatted file; returned if `return_obj` is
            False upon entry.

        yaml_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing all attributes
            injested from the YAML-formatted file; returned if
            `return_obj` is True upon entry.

        """

        # Define the YAML library loader type.
        YAMLLoader.add_constructor("!APPEND", YAMLLoader.append_constructor)
        YAMLLoader.add_implicit_resolver("!ENV", YAMLLoader.envvar_matcher, None)
        YAMLLoader.add_constructor("!ENV", YAMLLoader.envvar_constructor)
        YAMLLoader.add_constructor("!INC", YAMLLoader.include_constructor)

        # Open and read the contents of the specified YAML-formatted
        # file path.
        with open(yaml_file, "r", encoding="utf-8") as stream:
            # try:
            yaml_dict = yaml.load(stream, Loader=YAMLLoader)
            # except Exception:
            #    pass
            # yaml_dict = yaml.load_all(stream, Loader=FullLoader)

        # Define the Python data type to be returned; proceed
        # accordingly.
        yaml_return = None
        if return_obj:
            (attr_list, yaml_obj) = ([], parser_interface.object_define())
            for key in yaml_dict.keys():
                attr_list.append(key)
                value = parser_interface.dict_key_value(
                    dict_in=yaml_dict, key=key, no_split=True
                )
                yaml_obj = parser_interface.object_setattr(
                    object_in=yaml_obj, key=key, value=value
                )
            yaml_return = yaml_obj
        if not return_obj:
            yaml_return = yaml_dict

        return yaml_return

    def write_tmpl(
        self: Generic, yaml_dict: Dict, yaml_path: str, yaml_template: str
    ) -> None:
        """
        Description
        -----------

        This method ingests a YAML template file and parses a Python
        dictionary containing key and value pairs for template
        variables to be replaced; the updated template is then written
        to the user-specified path.

        Parameters
        ----------

        yaml_dict: ``Dict``

            A Python dictionary containing key and values pairs
            corresponding to the template variables within the
            user-specified YAML-formatted template file.

        yaml_template: ``str``

            A Python string specifying the template variables to seek
            and update.

        yaml_path: ``str``

            A Python string specifying the path to the YAML-formatted
            output file derived from the template.

        """

        # Read the template file.
        with open(yaml_template, "r", encoding="utf-8") as file:
            template = file.read().split("\n")

        # Open and write the namelist file while formatting the
        # template values specified upon entry accordingly.
        with open(yaml_path, "w", encoding="utf-8") as file:
            for item in template:
                for key in yaml_dict.keys():
                    if key in item:
                        value = parser_interface.dict_key_value(
                            dict_in=yaml_dict, key=key, no_split=True
                        )
                        item = item.replace(f"<{key}>", str(value))
                file.write(f"{item}\n")

    def write_yaml(
        self: Generic,
        yaml_file: str,
        in_dict: Dict,
        default_flow_style: bool = False,
        append: bool = False,
    ) -> None:
        """
        Description
        -----------

        This method writes a YAML Ain't Markup Language (e.g., YAML)
        formatted file using the specified Python dictionary.

        Parameters
        ----------

        yaml_file: ``str``

            A Python string containing the full-path to the YAML file
            to be written.

        in_dict: ``Dict``

            A Python dictionary containing the attributes to be
            written to the YAML file.

        Keywords
        --------

        default_flow_style: ``bool``, optional

            A Python boolean valued variable specifying the output
            YAML file formatting.

        append: ``bool``, optional

            A Python boolean valued variable specifying whether to
            append to an existing YAML-formatted file; if False upon
            entry any existing YAML-formatted file of the same
            yaml_file attribute name will be overwritten.

        """

        # Open and write the dictionary contents to the specified
        # YAML-formatted file path.
        if append:
            fileopt = "a"
        if not append:
            fileopt = "w"
        with open(yaml_file, fileopt, encoding="utf-8") as file:
            yaml.dump(in_dict, file, default_flow_style=default_flow_style)


# ----


class YAMLLoader(SafeLoader):
    """
    Description
    -----------

    This is the base-class object for all YAML file parsing
    interfaces; it is a sub-class of SafeLoader.

    """

    # Define the YAML library loader type; this follows from the
    # discussion found at https://tinyurl.com/yamlenvparse
    envvar_matcher = re.compile(r".*\$\{([^}^{]+)\}.*")

    def append_constructor(self: SafeLoader, node: ScalarNode) -> str:
        """
        Description
        -----------

        This method us the YAML value string append constructor.

        Parameters
        ----------

        node: ``ScalarNode``

            A Python ScalarNode variable containing the YAML
            attribute.

        Returns
        -------

        string: ``str``

            A Python string variable containing the contents of the
            respective list.

        """

        # Build the string and return the result.
        string = str()
        for item in node.value:
            try:
                string = string + item.value
            except TypeError:
                pass

        return string

    def envvar_constructor(self: SafeLoader, node: ScalarNode) -> Any:
        """
        Description
        -----------

        This method is the environment variable template constructor.

        Parameters
        ----------

        node: ``ScalarNode``

            A Python ScalarNode variable containing the YAML
            attribute.

        Returns
        -------

        return: ``Any``

            A Python Any type variable containing the expanded/updated
            YAML attribute(s) using the relevant environment
            variable(s).

        """

        # Expand and update the YAML attributes with the environment
        # variable value(s).
        return os.path.expandvars(node.value)

    def include_constructor(self: SafeLoader, node: ScalarNode) -> Any:
        """
        Description
        -----------

        This method is the file inclusion (i.e., opening and reading)
        template constructor.

        Parameters
        ----------

        node: ``ScalarNode``

            A Python ScalarNode variable containing the YAML
            attribute.

        Returns
        -------

        return: ``Any``

            A Python Any type variable containing the contents of the
            YAML-formatted file path.

        """

        # Load and return the contents of the YAML-formatted file
        # path.
        filename = self.construct_scalar(node)
        with open(filename, "r", encoding="utf-8") as file:
            return yaml.load(file, YAMLLoader)
