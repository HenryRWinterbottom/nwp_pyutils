"""
Module
------

    exceptions_interface.py

Description
-----------

    This module loads the exceptions package.

Classes
-------

    ArgumentsInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        utils/arguments_interface module; it is a sub-class of Error.

    AWSCLIInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/awscli_interface module; it is a sub-class of Error.

    Boto3InterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/boto3_interface module; it is a sub-class of Error.

    CLIInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        execute/cli_interface module; it is a sub-class of Error.

    ContainerInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        execute/container_interface module; it is a sub-class of
        Error.

    CurlInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/curl_interface module; it is a sub-class of Error.

    DateTimeInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        tools/datetime_interface module; it is a sub-class of Error.

    EnviroInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        confs/enviro_interface module; it is a sub-class of Error.

    ExecutableInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        execute/executable_interface module; it is a sub-class of
        Error.

    GithubInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/github_interface module; it is a sub-class of Error.

    GRIBInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/grib_interface module; it is a sub-class of Error.

    HashLibInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/hashlib_interface module; it is a sub-class of Error.

    Jinja2InterfaceError(msg)

        This is the base-class for exceptions encountered within the
        confs/jinja2_interface module; it is a sub-class of Error.

    JSONInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        confs/json_interface module; it is a sub-class of Error.

    NamelistInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        confs/namelist_interface module; it is a sub-class of Error.

    NetCDF4InterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/netcdf4_interface module; it is a sub-class of Error.

    NOAAHPSSInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/noaahpss_interface module; it is a sub-class of Error.

    ParserInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        tools/parser_interface module; it is a sub-class of Error.

    SchemaInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        utils/schema_interface module; it is a sub-class of Error.

    SQLite3InterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/sqlite3_interface module; it is a sub-class of Error.

    SubprocessInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        execute/subprocess_interface module; it is a sub-class of
        Error.

    TarFileInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/tarfile_interface module; it is a sub-class of Error.

    TCVitalsInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/tcvitalsinterface module; it is a sub-class of Error.

    TemplateInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        confs/template_interface module; it is a sub-class of Error.

    TimestampInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        utils/timestamp_interface module; it is a sub-class of Error.

    URLInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/url_interface module; it is a sub-class of Error.

    WgetInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/wget_interface module; it is a sub-class of Error.

    XArrayInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/xarray_interface module; it is a sub-class of Error.

    XMLInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        ioapps/xml_interface module; it is a sub-class of Error.

    YAMLInterfaceError(msg)

        This is the base-class for exceptions encountered within the
        confs/yaml_interface module; it is a sub-class of Error.

Author(s)
---------

    Henry R. Winterbottom; 28 December 2022

History
-------

    2022-12-28: Henry Winterbottom -- Initial implementation.

"""

# ----

from utils.error_interface import Error

# ----

# Define all available module properties.
__all__ = [
    "ArgumentsInterfaceError",
    "AWSCLIInterfaceError",
    "Boto3InterfaceError",
    "CLIInterfaceError",
    "ContainerInterfaceError",
    "CurlInterfaceError",
    "DateTimeInterfaceError",
    "EnviroInterfaceError",
    "ExecutableInterfaceError",
    "GithubInterfaceError",
    "GRIBInterfaceError",
    "HashLibInterfaceError",
    "Jinja2InterfaceError",
    "JSONInterfaceError",
    "NamelistInterfaceError",
    "NetCDF4InterfaceError",
    "NOAAHPSSInterfaceError",
    "ParserInterfaceError",
    "SchemaInterfaceError",
    "SQLite3InterfaceError",
    "SubprocessInterfaceError",
    "TarFileInterfaceError",
    "TCVitalsInterfaceError",
    "TemplateInterfaceError",
    "TimestampInterfaceError",
    "URLInterfaceError",
    "WgetInterfaceError",
    "XArrayInterfaceError",
    "XMLInterfaceError",
    "YAMLInterfaceError",
]

# ----


class ArgumentsInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/arguments_interface module; it is a sub-class of Error.

    """


# ----


class AWSCLIInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/awscli_interface module; it is a sub-class of Error.

    """


# ----


class Boto3InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/boto3_interface module; it is a sub-class of Error.

    """


# ----


class CLIInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    execute/cli_interface module; it is a sub-class of Error.

    """


# ----


class ContainerInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    execute/container_interface module; it is a sub-class of Error.

    """


# ----


class CurlInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/curl_interface module; it is a sub-class of Error.

    """


# ----


class DateTimeInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    tools/datetime_interface module; it is a sub-class of Error.

    """


# ----


class EnviroInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/enviro_interface module; it is a sub-class of Error.

    """


# ----


class ExecutableInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    execute/executable_interface module; it is a sub-class of Error.

    """

# ----


class GithubInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/github_interface module; it is a sub-class of Error.

    """


# ----


class GRIBInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/grib_interface module; it is a sub-class of Error.

    """


# ----


class HashLibInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/hashlib_interface module; it is a sub-class of Error.

    """


# ----


class Jinja2InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/jinja2_interface module; it is a sub-class of Error.

    """


# ----


class JSONInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/json_interface module; it is a sub-class of Error.

    """


# ----


class NamelistInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/namelist_interface module; it is a sub-class of Error.

    """


# ----


class NetCDF4InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/netcdf4_interface module; it is a sub-class of Error.

    """


# ----


class NOAAHPSSInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/noaahpss_interface module; it is a sub-class of Error.

    """


# ----


class ParserInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    tools/parser_interface module; it is a sub-class of Error.

    """


# ----


class SchemaInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/schema_interface module; it is a sub-class of Error.

    """


# ----


class SQLite3InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/sqlite3_interface module; it is a sub-class of Error.

    """


# ----


class SubprocessInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    execute/subprocess_interface module; it is a sub-class of Error.

    """


# ----


class TarFileInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/tarfile_interface module; it is a sub-class of Error.

    """


# ----


class TCVitalsInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/tcvitals_interface module; it is a sub-class of Error.

    """


# ----


class TemplateInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/template_interface module; it is a sub-class of Error.

    """


# ----


class TimestampInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/timestamp_interface module; it is a sub-class of Error.

    """


# ----


class URLInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/url_interface module; it is a sub-class of Error.

    """


# ----


class WgetInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/wget_interface module; it is a sub-class of Error.

    """


# ----


class XArrayInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/xarray_interface module; it is a sub-class of Error.

    """


# ----


class XMLInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/xml_interface module; it is a sub-class of Error.

    """


# ----


class YAMLInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    confs/yaml_interface module; it is a sub-class of Error.

    """
