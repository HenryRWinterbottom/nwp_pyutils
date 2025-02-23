"""
Module
------

    parser_interface.py

Description
-----------

    This module contains functions to perform various tasks which
    involve the parsing of dictionaries, lists, and other Python type
    comprehensions.

Functions
---------

    argspec(func)

       This function collects the attributes for a specified Callable
       object and returns a SimpleNamespace object containing the
       `argspec` attributes.

    dict_formatter(in_dict)

        This function formats a Python dictionary; all UNICODE and
        data-type conversions are performed within this function.

    dict_key_case(dict_in, lowercase=False, uppercase=False)

        This function appends either lower-, upper-, or both lower-
        and uppercase key and value pairs to the Python dictionary
        specified upon entry.

    dict_key_remove(dict_in, key):

        This function attempts to remove a Python dictionary key and
        value pair.

    dict_key_value(dict_in, key, force=False, max_value=False,
                   min_value=False, index_value=None, no_split=False)

        This function ingests a Python dictionary and a dictionary key
        and return the value(s) corresponding to the respective
        dictionary key; if the optional variable `force` is `True` and
        the dictionary key does not exist within the Python
        dictionary, the function will return NoneType.

    dict_merge(dict1, dict2)

        This function merges two Python dictionaries and returns a
        generator containing the merged Python dictionary relative to
        the checks within the function.

    dict_replace_value(in_dict, old, new)

        This function replaces strings within a (nested) Python
        dictionary and returns the updated (nested) Python dictionary.

    dict_toobject(in_dict)

        This funcction converts and returns the Python dictionary
        `in_dict`, specified upon entry, to a Python Namespace
        `out_obj`.

    enviro_get(envvar)

        This function retrieves the environment variable corresponding
        to the specified string; if the environment variable is not
        defined, NoneType is returned.

    enviro_set(envvar, value)

        This function defines the environment variable corresponding
        to the supported specified value.

    f90_bool(value)

        This method will transform boolean type values to a FORTRAN 90
        boolean format; if the variable `value` specified upon entry
        is not of boolean format the value is returned unaltered.

    find_commonprefix(strings_list)

        This function returns the common prefix from a list of strings.

    handler(func, handle: lambda errmsg: errmsg, return_none=False,
            raise_exception=False, *args, **kwargs):

        This method permits exceptions to raised(i.e., handled) within
        Python list comprehensions.

    import_func(app_obj)

        This function imports a Python function in accordance with the
        attributes collected from the SimpleNamespace object.

    list_get_type(in_list, dtype):

        This function parses a list and returns a list of values in
        accordance with the specified data type.

    list_replace_value(in_list, old, new)

        This function replaces strings within a Python list and
        returns the updated Python list; this function adapted from
        https://tinyurl.com/list-value-replace.

    match_list(in_list, match_string, exact=False):

        This function ingests a Python list and a Python string and
        matches, either exact or partial, are sought for the string
        within the provided; if `exact` is `True` upon entry, the
        matching Python string is returned if a match is found;
        otherwise NoneType is returned; if `exact` is `False` upon
        entry, a list of matching Python strings is returned.

    object_append(object_in, object_key, dict_in):

        This function appends the contents of Python dictionary to
        specified object key.

    object_compare(obj1, obj2)

        This function compares two Python SimpleNamespaces or objects.

    object_deepcopy(object_in):

        This function ingests a Python object and returns a deep copy of
        the respective object.

    object_define()

        This function defines an empty Python object.

    object_getattr(object_in, key, force=False)

        This function ingests a Python object and a Python attribute
        and returns the value of the respective attribute; if `force`
        is `True` and the Python object attribute does not exist, this
        function returns NoneType.

    object_hasattr(object_in, key)

        This function checks whether a Python object contains an
        attribute and returns an appropriate boolean value indicating
        the result of the inquiry.

    object_setattr(object_in, key, value)

        This function ingests a Python object and a Python key and value
        pair and defines the attributes for the respective object.

    object_todict(object_in)

        This function ingests a Python object and returns a Python
        dictionary containing the contents of the respective object.

    str_to_bool(string)

        This function converts a Python string to it's corresponding
        boolean value; if a JSONDecodeError exception is encountered,
        NoneType is returned.

    string_parser(in_list)

        This function ingests a Python list of variables and returns
        Python list of appropriately formatted values.

    true_or_false(argval)

        This function checks whether an argument is a Boolean-type
        value; if so, this function defines the appropriate Python
        boolean-type; otherwise, this function returns NoneType.

    unique_list(in_list)

        This function ingests a list, possibly with duplicate values,
        and returns a list of only unique values.

    update_dict(default_dict, base_dict, update_none=False)

        This function reads Python dictionaries containing default key
        and value pairs (`default_dict`) and a base (optional or
        changed values) Python dictionary containing key and value
        pairs (`base_dict`); the output Python dictionary
        `output_dict` is initialized with the base Python dictionary;
        any key and value pairs within `default_dict` which are not in
        `output_dict` are updated with those from `default_dict`.

Author(s)
---------

    Henry R. Winterbottom; 21 August 2022

History
-------

    2022-08-21: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=fixme
# pylint: disable=keyword-arg-before-vararg
# pylint: disable=raise-missing-from
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-lines
# pylint: disable=undefined-variable
# pylint: disable=unnecessary-comprehension

# ----

import collections
import copy
import inspect
import json
import os
from importlib import import_module
from json.decoder import JSONDecodeError
from types import SimpleNamespace
from typing import Any, Callable, Dict, Generator, List, Tuple, Union

import numpy
from utils.exceptions_interface import ParserInterfaceError

# ----

# Define all available module properties.
__all__ = [
    "argspec",
    "dict_formatter",
    "dict_key_case",
    "dict_key_remove",
    "dict_key_value",
    "dict_merge",
    "dict_replace_value",
    "dict_toobject",
    "enviro_get",
    "enviro_set",
    "f90_bool",
    "find_commonprefix",
    "handler",
    "import_func",
    "list_get_type",
    "list_replace_value",
    "match_list",
    "object_append",
    "object_compare",
    "object_deepcopy",
    "object_define",
    "object_getattr",
    "object_hasattr",
    "object_setattr",
    "object_todict",
    "str_to_bool",
    "string_parser",
    "true_or_false",
    "unique_list",
    "update_dict",
]

# ----


def argspec(func: Callable) -> SimpleNamespace:
    """
    Description
    -----------

    This function collects the attributes for a specified Callable
    object and returns a SimpleNamespace object containing the
    `argspec` attributes.

    Parameters
    ----------

    func: ``Callable``

        A Python Callable function from which to collect the
        respective allowable arguments.

    Returns
    -------

    argspec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the Callable
        function object allowable arguments.

    """

    # Collect all attributes for the respective Callable object.
    argspec_obj = SimpleNamespace(**inspect.getfullargspec(func)._asdict())

    return argspec_obj


# ----


def dict_formatter(in_dict: Dict) -> Dict:
    """
    Description
    -----------

    This function formats a Python dictionary; all UNICODE and
    data-type conversions are performed within this function.

    Parameters
    ----------

    in_dict: ``Dict``

        A standalone Python dictionary to be formatted.

    Returns
    -------

    out_dict: ``Dict``

        A standalone Python dictionary which has been formatted.

    """

    # Define local function to sort and format the input Python
    # dictionary upon entry.
    def sorted_by_keys(
        dct,
    ):
        new_dct = collections.OrderedDict()
        for key, value in sorted(dct.items(), key=lambda key: key):
            if isinstance(value, dict):
                new_dct[key] = sorted_by_keys(value)
            else:
                test_value = value
                if isinstance(test_value, bool):
                    if test_value:
                        value = True
                    if not test_value:
                        value = False
                if isinstance(test_value, str):
                    try:
                        dummy = float(test_value)
                        if "." in test_value:
                            value = float(test_value)
                        else:
                            value = int(test_value)
                    except ValueError:
                        if test_value.lower() == "none":
                            value = None
                        elif test_value.lower() == "true":
                            value = True
                        elif test_value.lower() == "false":
                            value = False
                        else:
                            value = str(test_value)
                new_dct[key] = value

        return new_dct

    # Define the formatted output dictionary.
    out_dict = sorted_by_keys(dct=in_dict)

    return out_dict


# ----


def dict_key_case(
    dict_in: Dict, lowercase: bool = False, uppercase: bool = False
) -> Dict:
    """
    Description
    -----------

    This function appends either lower-, upper-, or both lower- and
    uppercase key and value pairs to the Python dictionary specified
    upon entry.

    Parameters
    ----------

    dict_in: ``Dict``

        A Python dictionary to be updated.

    Keywords
    --------

    lower: ``bool``, optional

        A Python boolean valued variable specifying whether to append
        lowercase key and value pairs to the Python dictionary
        specified upon entry.

    upper: ``bool``, optional

        A Python boolean valued variable specifying whether to append
        uppercase key and value pairs to the Python dictionary
        specified upon entry.

    Returns
    -------

    dict_out: ``Dict``

        An updated Python dictionary; if both `lowercase` and
        `uppercase` are `False` upon entry, `dict_in` specified upon
        entry is returned.

    """

    # Update the Python dictionry specified upon entry accordingly.
    dict_out = dict_in
    if lowercase:
        dict_out = dict(
            dict_out, **({key.lower(): value for (key, value) in dict_out.items()})
        )
    if uppercase:
        dict_out = dict(
            dict_out, **({key.upper(): value for (key, value) in dict_out.items()})
        )

    return dict_out


# ----


def dict_key_remove(dict_in: Dict, key: str) -> Dict:
    """
    Description
    -----------

    This function attempts to remove a Python dictionary key and value
    pair.

    Parameters
    ----------

    dict_in: ``Dict``

        A Python dictionary to be parsed.

    key: ``str``

        A Python string indicating the dictionary key within the
        Python dictionary (see above).

    Returns
    -------

    dict_in: ``Dict``

        A Python dictionary from which the specified key and value
        pair has been removed (if present in the Python dictionary on
        entry).

    """

    # Attempt to remove the dictionary value corresponding to the key
    # specified upon entry.
    try:
        del dict_in[key]
    except KeyError:
        pass

    return dict_in


# ----


def dict_key_value(
    dict_in: Dict,
    key: str,
    force: bool = False,
    max_value: bool = False,
    min_value: bool = False,
    index_value: int = None,
    no_split: bool = False,
) -> Union[List, Any]:
    """
    Description
    -----------

    This function ingests a Python dictionary and a dictionary key and
    return the value(s) corresponding to the respective dictionary
    key; if the optional variable `force` is True and the dictionary
    key does not exist within the Python dictionary, the function will
    return NoneType.

    Parameters
    ----------

    dict_in: ``Dict``

        A Python dictionary to be parsed.

    key: ``str``

        A Python string indicating the dictionary key within the
        Python dictionary (see above).

    Keywords
    --------

    force: ``str``, optional

        A Python boolean variable; if True and in the absence of the
        respective dictionary key within the Python dictionary,
        NoneType is returned.

    max_value: ``bool``, optional

        A Python boolean variable; if True, and a Python list yielded
        via the Python dictionary key, the maximum value within the
        Python list will be returned; the default value is False.

    min_value: ``bool``, optional

        A Python boolean variable; if True, and a Python list yielded
        via the Python dictionary key, the minimum value within the
        Python list will be returned; the default value is False.

    index_value: ``int``, optional

        A Python integer defining the index within the Python list (as
        yielded by the Python dictionary key) to return; the default
        value is NoneType.

    no_split: ``bool``, optional

        A Python boolean variable; if True and if a string, the string
        will not be split into and returned as a comma-delimited list.

    Returns
    -------

    value: ``Union[List, Any]``

        A list of values collected from the ingested Python dictionary
        and the respective dictionary key if `no_split` is False; a
        string otherwise.

    Raises
    ------

    ParserInterfaceError:

        - raised if both minimum and maximum values of a list are
          requested; only minimum or only maximum may be requested
          upon entry.

        - raised if the keyword argument combinations passed upon
          entry are incorrect.

    """

    # Check that the parameter values are valid.
    if max_value and min_value:
        msg = (
            "The user has requested both minimum and maximum list "
            "value; please check that only one threshold value is "
            "is to be sought from the list. Aborting!!!"
        )
        raise ParserInterfaceError(msg=msg)
    if index_value is not None:
        if max_value:
            msg = (
                "The user has selected both a single value (as per "
                "the specified index) and the maximum list value; "
                "please check which criteria to fulfill. Aborting!!!"
            )
            raise ParserInterfaceError(msg=msg)
        if min_value:
            msg = (
                "The user has selected both a single value (as per "
                "the specified index) and the minimum list value; "
                "please check which criteria to fulfill. Aborting!!!"
            )
            raise ParserInterfaceError(msg=msg)

    # Collect the dictionary attribute value; proceed accordingly.
    try:
        value = dict_in[key]
        if no_split:
            return value
        try:
            in_list = dict_in[key].split(",")
            value = list(string_parser(in_list=in_list))
            if max_value:
                value = max(value)
            if min_value:
                value = min(value)
            if index_value is not None:
                value = value[index_value]
        except AttributeError:
            value = dict_in[key]
    except KeyError:
        if not force:
            msg = (
                f"Key {key} could not be found in user provided dictionary. "
                "Aborting!!!"
            )
            raise ParserInterfaceError(msg=msg)
        if force:
            value = None

    return value


# ----


def dict_merge(
    dict1: Dict, dict2: Dict, lowercase: bool = False, uppercase: bool = False
) -> Generator:
    """
    Description
    -----------

    This function merges two Python dictionaries and returns a
    generator containing the merged Python dictionary relative to the
    checks within the function.

    Parameters
    ----------

    dict1: ``Dict``

        A Python dictionary to be merged.

    dict2: ``Dict``

        A Python dictionary to be merged.

    Keywords
    --------

    lower: ``bool``, optional

        A Python boolean valued variable specifying whether to append
        lowercase key and value pairs to the Python dictionary
        specified upon entry.

    upper: ``bool``, optional

        A Python boolean valued variable specifying whether to append
        uppercase key and value pairs to the Python dictionary
        specified upon entry.

    Yields
    ------

    ``Generator``:

        A Python Generator containing the contents of `dict1` and
        `dict2`.

    """

    # Define the attributes list containing the unique values from the
    # respective Python dictionaries.
    dict1 = dict_key_case(dict_in=dict1, lowercase=lowercase, uppercase=uppercase)
    dict2 = dict_key_case(dict_in=dict2, lowercase=lowercase, uppercase=uppercase)
    attrs_list = set(dict1.keys()).union(dict2.keys())
    for k in attrs_list:
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(dict_merge(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


# ----


def dict_replace_value(in_dict: Dict, old: str, new: str) -> Dict:
    """
    Description
    -----------

    This function replaces strings within a (nested) Python dictionary
    and returns the updated (nested) Python dictionary; this function
    adapted from https://tinyurl.com/dict-value-replace.

    Parameters
    ----------

    in_dict: ``Dict``

        A (nested) Python dictionary containing Python strings to be
        replaced/updated.

    old: ``str``

        A Python string value specifying the Python string instance to
        be replaced.

    new: ``str``

        A Python string value specifying the Python string to replace
        the value specified by the `old` attribute.

    Returns
    -------

    out_dict: ``Dict``

        A (nested) Python dictionary updated in accordance within the
        attributes specified by the `old` and `new` attributes;
        otherwise this Python dictionary is identical to that defined
        by `in_dict`.

    """

    # Parse the Python dictionary and update an dictionary instances.
    out_dict = {}
    for key, value in in_dict.items():
        if isinstance(value, dict):
            value = dict_replace_value(value, old, new)
        elif isinstance(value, list):
            value = list_replace_value(value, old, new)
        elif isinstance(value, str):
            value = value.replace(old, new)
        out_dict[key] = value

    return out_dict


# ----


def dict_toobject(in_dict: Dict) -> SimpleNamespace:
    """
    Description
    -----------

    This funcction converts and returns the Python dictionary
    `in_dict`, specified upon entry, to a Python Namespace `out_obj`.

    Parameters
    ----------

    in_dict: ``Dict``

        A Python dictionary containing the attribute key and value
        pairs to be cast as a Python Namespace.

    Returns
    -------

    out_obj: ``SimpleNamespace``

        A Python SimpleNamespace defined by casting the Python
        dictionary `in_dict` specified upon input to the respective
        Python SimpleNamespace.

    """

    # Define the Python namespace
    out_obj = SimpleNamespace(**in_dict)

    return out_obj


# ----


def enviro_get(envvar: str) -> Union[bool, float, int, str]:
    """
    Description
    -----------

    This function retrieves the environment variable corresponding to
    the specified string; if the environment variable is not defined,
    NoneType is returned.

    Parameters
    ----------

    envvar: ``str``

        A Python string specifying the environment variable name.

    Returns
    -------

    envvarval: ``Union[bool, float, int, str]``

        A Python type that contains the query for the environment
        variable.

    """

    # Parse the run-time environment and return the attributes of the
    # environment variable specified upon entry.
    if envvar in os.environ:
        envvarval = os.environ.get(envvar)
    else:
        envvarval = None

    return envvarval


# ----


def enviro_set(envvar: str, value: Union[Any]) -> None:
    """
    Description
    -----------

    This function defines the environment variable corresponding to
    the supported specified value.

    Parameters
    ----------

    envvar: ``str``

        A Python string specifying the environment variable name.

    value: ``Union[Any]``

        A Python value specifying the value of the environment
        variable.

    """

    # Define the run-time environment variable.
    if isinstance(value, list):
        os.environ[envvar] = ",".join([item for item in value])
    if not isinstance(value, list):
        os.environ[envvar] = value


# ----


def f90_bool(value: Any) -> Any:
    """
    Description
    -----------

    This method will transform boolean type values to a FORTRAN 90
    boolean format; if the variable `value` specified upon entry is
    not of boolean format the value is returned unaltered.

    Parameters
    ----------

    value: ``Any``

        A Python variable to be evaluated as a boolean type value; if
        a boolean type the corresponding value is returned as a
        FORTRAN 90 boolean format.

    Returns
    -------

    value: ``Any``

        An evaluated Python variable; if `value` was boolean type upon
        entry the returned value is of FORTRAN 90 boolean format; if
        not, the unaltered input value is returned.

    """

    # Check the type for the respective input value; proceed
    # accordingly.
    if isinstance(value, bool):
        if value:
            value = "T"
        if not value:
            value = "F"

    return value


# ----


def find_commonprefix(strings_list: List) -> str:
    """
    Description
    -----------

    This function returns the common prefix from a list of strings.

    Parameters
    ----------

    strings_list: ``List``

        A Python list of strings

    Returns
    -------

    common_prefix: ``str``

        A Python string specifying the common prefix determined from a
        list of Python strings; NoneType if a common prefix cannot be
        determined.

    """

    # Seek common prefix values from the list of strings specified
    # upon entry.
    common_prefix = None
    if strings_list:
        common_prefix = os.path.commonprefix(strings_list)

    return common_prefix


# ----


def handler(
    func: Callable,
    handle=lambda errmsg: errmsg,
    return_none: bool = False,
    raise_exception: bool = False,
    *args,
    **kwargs,
) -> Union[Any, None, Exception]:
    """
    Description
    -----------

    This method permits exceptions to raised (i.e., handled) within
    Python list comprehensions.

    Parameters
    ----------

    func: ``Callable``

        A Python function, often nested within a Python list
        comprehension, to be evaluated.

    handle: ``Callable``

        A Python lambda function to be evaluated within the list
        comprehension.

    Keywords
    --------

    return_none: ``bool``, optional

        A Python boolean valued variable specifying whether to return
        None if an exception is encountered.

    raise_exception: ``bool``, optional

        A Python boolean values variable specifying to whether to
        raise the exception encountered while evaluating the function
        within the Python list comprehension.

    Other Parameters
    ----------------

    args: ``Tuple``, optional

        Python type arguments to be passed to the respective Python
        function `func`.

    kwargs: ``Dict``, optional

        Python type keyword arguments to be passed to the respective
        Python function `func`.

    Returns
    -------

    value: ``Union[Any, None, Exception]``

        A Python variable type containing the returned expression from
        the Python list evaluation of a function (`func`).

    """

    # Evaluate the function nested within a Python list comprehension;
    # proceed accordingly.
    try:
        value = func(*args, **kwargs)
    except Exception as errmsg:
        if return_none:
            value = None
        if raise_exception:
            value = handle(errmsg)

    return value


# ----


def import_func(app_obj: SimpleNamespace) -> Union[None, Callable]:
    """
    Description
    -----------

    This function imports a Python function in accordance with the
    attributes collected from the SimpleNamespace object.

    Parameters
    ----------

    app_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        the respective Callable object to return.

    Returns
    -------

    func: ``Union[None, Callable]``

        A Python Callable object containing the requested function; if
        the function cannot be determined, NoneType is returned.

    """

    # Define the Python function; if one cannot be determined, return
    # `NoneType`.
    attr_list = ["cls", "func", "module"]
    for attr in attr_list:
        app_obj = object_setattr(
            object_in=app_obj,
            key=attr,
            value=object_getattr(object_in=app_obj, key=attr, force=True),
        )
    func = None
    if app_obj.cls is None:
        if app_obj.func is not None:
            module = import_module(app_obj.module)
            func = object_getattr(object_in=module, key=app_obj.func)
    else:
        pass  # TODO: Add support for importing methods from classes.

    return func


# ----


def list_get_type(in_list: List, dtype: str) -> List:
    """
    Description
    -----------

    This function parses a list and returns a list of values in
    accordance with the specified data type.

    Parameters
    ----------

    in_list: ``List``

        A Python list containing values possibly of various data
        types.

    dtype: ``str``

        A Python string specifying the data type to be sought.

    Returns
    -------

    var_list: ``List``

        A Python list contain values collected from the input list but
        of the specified data type.

    """

    # Find all items within the list specified upon entry of a
    # specified data type upon entry.
    var_list = []
    try:
        for item in in_list:
            if isinstance(item, dtype):
                var_list.append(item)
    except TypeError:
        var_list.append(numpy.nan)

    return var_list


# ----


def list_replace_value(in_list: List, old: str, new: str) -> List:
    """
    Description
    -----------

    This function replaces strings within a Python list and returns
    the updated Python list; this function adapted from
    https://tinyurl.com/list-value-replace.

    Parameters
    ----------

    in_list: ``List``

        A Python list containing Python strings to be
        replaced/updated.

    old: ``str``

        A Python string value specifying the Python string instance to
        be replaced.

    new: ``str``

        A Python string value specifying the Python string to replace
        the value specified by the `old` attribute.

    Returns
    -------

    out_list: ``List``

        A Python list updated in accordance within the attributes
        specified by the `old` and `new` attributes; otherwise this
        Python list is identical to that defined by `in_list`.

    """

    # Parse the Python dictionary and update the respective instances.
    out_list = []
    for item in in_list:
        if isinstance(item, list):
            item = list_replace_value(item, old, new)
        elif isinstance(item, dict):
            item = dict_replace_value(item, old, new)
        elif isinstance(item, str):
            item = item.replace(old, new)
        out_list.append(item)

    return out_list


# ----


def object_append(
    object_in: SimpleNamespace, object_key: str, dict_in: Dict
) -> SimpleNamespace:
    """
    Description
    -----------

    This function appends the contents of Python dictionary to
    specified object key.

    Parameters
    ----------

    object_in: ``SimpleNamespace``

        A Python SimpleNamespace or object to be appended.

    object_key: ``str``

        A Python string value specifying the input Python object
        attribute.

    dict_in: ``Dict``

        A Python dictionary containing the key and value pairs to
        append to the input Python object.

    Returns
    -------

    object_out: ``SimpleNamespace``

        A Python SimpleNamespace or object containing the appended
        input Python dictionary key and value pairs relative to the
        specified Python object attribute.

    """

    # Define the output object and the Python dictionary in accordance
    # with the arguments provided upon entry.
    object_out = object_in
    object_dict = object_getattr(object_in=object_in, key=object_key)
    for key in dict_in.keys():
        value = dict_key_value(dict_in=dict_in, key=key, no_split=True)
        object_dict[key] = value
    object_out = object_setattr(object_in=object_out, key=object_key, value=object_dict)

    return object_out


# ----


def object_compare(
    obj1: Union[SimpleNamespace, object], obj2: Union[SimpleNamespace, object]
) -> bool:
    """
    Description
    -----------

    This function compares two Python SimpleNamespaces or objects.

    Parameters
    ----------

    obj1: ``Union[SimpleNamespace, object]``

        A Python SimpleNamespace or object against which to compare
        with another SimpleNamespace or object.

    obj2: ``Union[SimpleNamespace, object]``

        A Python SimpleNamespace or object to compare to `obj1` (above).

    Returns
    -------

    compare: ``bool``

        A Python boolean variable specifying whether the respective
        Python objects are identical.

    """

    # Compare the Python objects provided upon entry.
    compare = obj1 == obj2

    return compare


# ----


def object_deepcopy(
    object_in: Union[SimpleNamespace, object]
) -> Union[SimpleNamespace, object]:
    """
    Description
    -----------

    This function ingests a Python object and returns a deep copy of
    the respective object.

    Parameters
    ----------

    object_in: ``Union[SimpleNamespace, object]``

        A Python object for which to create a deep copy.

    Returns
    -------

    object_out: ``Union[SimpleNamespace, object]``

        A Python object which is a deep copy of the specified input
        object `object_in`.

    """

    # Create and return a deep copy of the Python object provided upon
    # entry.
    object_out = copy.deepcopy(object_in)

    return object_out


# ----


def object_define() -> SimpleNamespace:
    """
    Description
    -----------

    This function defines an empty Python SimpleNamespace object.

    Returns
    -------

    empty_obj: ``SimpleNamespace``

        An empty Python SimpleNamespace object.

    """

    # Initialize an empty Python object/namespace.
    empty_obj = SimpleNamespace()

    return empty_obj


# ----


def object_getattr(
    object_in: Union[SimpleNamespace, object], key: str, force: bool = False
) -> Any:
    """
    Description
    -----------

    This function ingests a Python object and a Python attribute and
    returns the value of the respective attribute; if `force` is
    `True` and the Python object attribute does not exist, this
    function returns NoneType.

    Parameters
    ----------

    object_in: ``Union[SimpleNamespace, object]``

        A Python SimpleNamespace or object within which to search for
        attributes.

    key: ``str``

        A Python string value specifying the attribute to seek.

    Keywords
    --------

    force: ``bool``, optional

        A Python boolean variable; if `True` and in the absence of the
        respective attribute within the Python object, NoneType is
        returned.

    Returns
    -------

    value: ``Any``

        The result of the respective attribute search.

    Raises
    ------

    ParserInterfaceError:

        - raised if `force` is `False` and the Python object attribute
          does not exist.

    """

    # Check whether the Python object passed upon entry contains the
    # key specified upon entry.
    if hasattr(object_in, key):
        value = getattr(object_in, key)
    if not hasattr(object_in, key):
        if force:
            value = None
        if not force:
            msg = (
                f"The object {object_in} does not contain attribute "
                f"{key}. Aborting!!!"
            )
            raise ParserInterfaceError(msg=msg)

    return value


# ----


def match_list(
    in_list: List, match_string: str, exact: bool = False
) -> Tuple[bool, str]:
    """
    Description
    -----------

    This function ingests a Python list and a Python string and
    matches, either exact or partial, are sought for the string within
    the provided; if `exact` is True upon entry, the matching Python
    string is returned if a match is found; otherwise NoneType is
    returned; if `exact` is False upon entry, a list of matching
    Python strings is returned.

    Parameters
    ----------

    in_list: ``List``

        A Python list of strings within matches will be sought.

    match_string: ``str``

        A Python string for which to search for matches within the
        ingested list.

    Keywords
    --------

    exact: ``bool``, optional

        A Python boolean variable; if True, a Python string will be
        returned assuming a match is made; if False, a Python list of
        strings matching `match_string` will be returned assuming
        matches can be made.

    Returns
    -------

    match_chk: ``bool``

        A Python boolean variable indicating whether a match (or
        matches) has (have) been made.

    match_str: ``str``

        A Python string (if `exact` is True upon entry) or a Python
        list of strings (if `exact` is False upon entry) containing
        all matches to the input match string; if no matches can be
        found, either NoneType (if `exact` is True upon entry) or an
        empty list (if `exact` is False upon entry) is returned.

    """

    # Define the local lists to be used for the matching application.
    lower_list = [word for word in in_list if word.islower()]
    upper_list = [word for word in in_list if word.isupper()]
    mixed_list = [word for word in in_list if not word.islower() and not word.isupper()]
    match_chk = False

    # If appropriate, seek exact matches; proceed accordingly.
    if exact:
        match_str = None
        for string in lower_list:
            if match_string.lower() == string.lower():
                match_chk = True
                match_str = string
                break
        for string in upper_list:
            if match_string.lower() in string.lower():
                match_chk = True
                match_str = string
                break
        for string in mixed_list:
            if match_string.lower() == string.lower():
                match_chk = True
                match_str = string
                break

    # If appropriate, seek non-exact matches; proceed accordingly.
    if not exact:
        match_str = []
        for string in lower_list:
            if match_string.lower() in string.lower():
                match_str.append(string)
        for string in upper_list:
            if match_string.lower() in string.lower():
                match_str.append(string)
        for string in mixed_list:
            if match_string.lower() in string.lower():
                match_str.append(string)
        if len(match_str) > 0:
            match_chk = True

    return (match_chk, match_str)


# ----


def object_hasattr(object_in: Union[SimpleNamespace, object], key: str) -> bool:
    """
    Description
    -----------

    This function checks whether a Python object contains an attribute
    and returns an appropriate boolean value indicating the result of
    the inquiry.

    Parameters
    ----------

    object_in: ``Union[SimpleNamespace, object]``

        A Python SimpleNamespace or object within which to inquire
        about attributes.

    key: ``str``

        A Python string value specifying the attribute to inquire
        about.

    Returns
    -------

    chk_attr: ``bool``

        A Python boolean value containing the result of the attribute
        inquiry.

    """

    # Check whether the Python object specified upon entry contains
    # the key specified upon entry.
    chk_attr = hasattr(object_in, key)

    return chk_attr


# ----


def object_setattr(
    object_in: Union[SimpleNamespace, object],
    key: str,
    value: Any,
) -> Union[SimpleNamespace, object]:
    """
    Description
    -----------

    This function ingests a Python SimpleNamespace or object and a
    Python key and value pair and defines the attributes for the
    respective SimpleNamespace or object.

    Parameters
    ----------

    object_in: ``Union[SimpleNamespace, object]``

        A Python SimpleNamespace or object within which to search for
        attributes.

    key: ``str``

        A Python string value specifying the attribute to define.

    value: ``Any``

        A Python variable value specifying the value to accompany the
        Python object attribute (`key`).

    Returns
    -------

    object_out: ``Union[SimpleNamespace, object]``

       A Python SimpleNamespace or object containing the specified key
       and value pair (e.g., attribute).

    """

    # Copy the Python object specified upon entry and define the new
    # attribute using the key and value pair specified upon entry.
    object_out = object_in
    setattr(object_out, key, value)

    return object_out


# ----


def object_todict(object_in: Union[SimpleNamespace, object]) -> Dict:
    """
    Description
    -----------

    This function ingests a Python SimpleNamespace or object and
    returns a Python dictionary containing the contents of the
    SimpleNamespace or object.

    Parameters
    ----------

    object_in: ``Union[SimpleNamespace, object]``

        A Python SimpleNamespace or object containing specified
        content.

    Returns
    -------

    dict_out: ``Dict``

        A Python dictionary containing the contents of the Python
        SimpleNamespace or object.

    """

    # Build a Python dictionary containing the contents of the Python
    # SimpleNamespace or object specified upon entry.
    dict_out = vars(object_in)

    return dict_out


# ----


def singletrue(bool_list: List) -> bool:
    """
    Description
    -----------

    This function ingests a list of boolean (e.g., logical) variables
    (`bool_list`) and returns True if a single true value is in the
    boolean list or False otherwise.

    Parameters
    ----------

    bool_list: ``List``

        A Python list of boolean type variables.

    Returns
    -------

    check: ``bool``

        A Python boolean variable specifying whether only a single
        True value is within the respective boolean list; if so, True
        is returned; otherwise False is returned.

    """

    # Build a generator function using the list of boolean variables
    # specified upon entry.
    iterator = iter(bool_list)
    has_true = any(iterator)
    has_another_true = any(iterator)
    check = has_true and not has_another_true

    return check


# ----


def str_to_bool(string: str) -> bool:
    """
    Description
    -----------

    This function converts a Python string to it's corresponding
    boolean value; if a JSONDecodeError exception is encountered,
    NoneType is returned.

    Parameters
    ----------

    string: ``str``

        A Python string for which to convert to a corresponding
        boolean value.

    Returns
    -------

    boolval: ``bool``

        A Python boolean valued variable containing the boolean value
        corresponding to the Python string specified upon entry; if a
        JSONDecodeError is encounterd, NoneType is returned.

    """

    # Convert the string value to it's corresponding boolean value;
    # proceed accordingly.
    try:
        boolval = json.loads(string.lower())
    except JSONDecodeError:
        boolval = None

    return boolval


# ----


def string_parser(in_list: List, remove_comma: bool = False) -> List:
    """
    Description
    -----------

    This function ingests a Python list of variables and returns a
    Python list of appropriately formatted values.

    Parameters
    ----------

    in_list: ``List``

        A Python list of variable values to be formatted.

    Keywords
    --------

    remove_comma: ``bool``, optional

        A Python boolean variable specifying to remove any comma
        string occurances in the returned list (see `out_list`).

    Returns
    -------

    out_list: ``List``

        A Python list of appropriately formatted variable values.

    """

    # Initialize and build the output list.
    out_list = []
    try:
        for value in in_list:
            test_value = value
            try:
                if isinstance(test_value, str):
                    test_value = test_value.encode("ascii", "ignore")
            except NameError:
                pass

            # Boolean-type variable instances.
            if isinstance(test_value, bool):
                if test_value:
                    value = True
                    if not test_value:
                        value = False

            # String-type variable instances.
            if isinstance(test_value, str):
                try:
                    dummy = float(test_value)
                    if "." in test_value:
                        value = float(test_value)
                    else:
                        value = int(test_value)

                # Update any values passed as strings accordingly.
                except ValueError:
                    if test_value.lower() == "none":
                        value = None
                    elif test_value.lower() == "true":
                        value = True
                    elif test_value.lower() == "false":
                        value = False
                    else:
                        value = str(test_value)
            try:
                value = value.rsplit()[0]
            except AttributeError:
                pass
            out_list.append(value)
    except TypeError:
        value = None
        out_list.append(value)

    # Update the output list accordingly.
    if remove_comma:
        new_list = []
        for item in out_list:
            if item != ",":
                new_list.append(item)
        out_list = new_list

    return out_list


# ----


def true_or_false(argval: Any) -> Union[bool, None]:
    """
    Description
    -----------

    This function checks whether an argument is a Boolean-type value;
    if so, this function defines the appropriate Python boolean-type;
    otherwise, this function returns NoneType.

    Parameters
    ----------

    argval: ``Any``

        A value corresponding to an argument.

    Returns
    -------

    pytype: ``Union[bool, None]``

        A Python boolean-type value if the argument is a boolean
        variable; otherwise, NoneType.

    """

    # Check the arguments provided upon entry and proceed accordingly.
    string = str(argval).upper()
    if "TRUE".startswith(string):
        pytype = True
    elif "FALSE".startswith(string):
        pytype = False
    else:
        pytype = None

    return pytype


# ----


def unique_list(in_list: List) -> List:
    """
    Description
    -----------

    This function ingests a list, possibly with duplicate values, and
    returns a list of only unique values.

    Parameters
    ----------

    in_list: ``List``

        A N-dimensional Python list containing strings.

    Returns
    -------

    out_list: ``List``

        A Python list containing only uniquely-valued strings.

    """
    out_list = []
    out_dict = collections.OrderedDict.fromkeys(x for x in in_list if x not in out_list)
    out_list = []
    for key in sorted(out_dict.keys()):
        out_list.append(key.replace(" ", ""))

    return out_list


# ----


def update_dict(default_dict: Dict, base_dict: Dict, update_none: bool = False) -> Dict:
    """
    Description
    -----------

    This function reads Python dictionaries containing default key and
    value pairs (`default_dict`) and a base (optional or changed
    values) Python dictionary containing key and value pairs
    (`base_dict`); the output Python dictionary `output_dict` is
    initialized with the base Python dictionary; any key and value
    pairs within `default_dict` which are not in `output_dict` are
    updated with those from `default_dict`.

    Parameters
    ----------

    default_dict: ``Dict``

        A Python dictionary containing default key and value pairs;
        this Python dictionary contains all possible key and value
        pairs to compute the output dictionary (`output_dict`).

    base_dict: ``Dict``

        A Python dictionary containing either optional or changed key
        and value pairs; this Python dictionary is used to initialize
        the output Python dictionary `output_dict`.

    Keywords
    --------

    update_none: ``bool``, optional

        A Python boolean valued variable specifying whether to update
        the output Python dictionary `output_dict` with None-type
        value occurances within the default Python dictionary
        `default_dict`.

    Returns
    -------

    output_dict: ``Dict``

        A Python dictionary containing the respective attributes from
        the base and default Python dictionaries, `base_dict` and
        `default_dict` respectively.

    """

    # Initialize the output Python dictionary.
    output_dict = base_dict

    # For any keys missing from the base Python dictionary
    # `base_dict`, update with the key and value pairs from the
    # default Python dictionary `default_dict`.
    for key in default_dict:
        if key not in output_dict:
            # Collect the key and value pair and update the Python
            # dictionary accordingly.
            value = dict_key_value(
                dict_in=default_dict, key=key, force=True, no_split=True
            )
            if update_none:
                if value is None:
                    pass
            if not update_none:
                output_dict[key] = value

    return output_dict
