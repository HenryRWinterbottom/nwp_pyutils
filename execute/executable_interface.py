"""
Module
------

    executable_interface.py

Description
-----------

    This module contains functions to launch executable applications
    either using the host platform or a specified Singularity image
    environment; both stand-alone executable applications as well as
    Singularity container applications are supported.

Functions
---------

    __check_exectype__(exec_obj)

        This function checks the application type (e.g., `serial`
        versus `multi` processor task allocations) and assigns the
        number of allotted tasks accordingly.

    __check_sifimg__(exec_obj)

        This function validates (any) Singularity image attributes.

    __get_cmd__(exec_obj)

        This function builds the `subprocess` command list.

    __get_nprocs_flag__(exec_obj)

        This function defines the respective scheduler flag for
        specifying the `number of processors` for the respective
        application.

    __redirect__(exec_obj)

        This function is a `contextmanager` to redirect standard error
        and standard output to specified file paths.

    __launcher(exec_obj)

        This function determines the executable application launcher.

    __run(exec_obj)

        This function executes the run-time for the respective
        application.

    __schema(exec_obj)

        This function defines the path to the YAML-formatted file
        containing the executable application schema.

    __setup(exec_obj)

        This function initializes the Python SimpleNamespace object in
        accordance with both the executable application schema and the
        attributes specified upon entry.

    __validate(exec_obj)

        This function validates the schema for the respective
        executable application.

    app_exec(func)

        This function is a wrapper function for an executable
        application.

Author(s)
---------

    Henry R. Winterbottom; 01 December 2023

History
-------

    2023-12-01: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-with
# pylint: disable=fixme
# pylint: disable=unused-variable

# ----

import functools
import inspect
import os
import subprocess
from contextlib import contextmanager
from types import SimpleNamespace
from typing import IO, Callable, Dict, Generator, Tuple

from confs.yaml_interface import YAML
from tools import fileio_interface, parser_interface, system_interface
from utils.exceptions_interface import ExecutableInterfaceError
from utils.logger_interface import Logger
from utils.schema_interface import build_schema, validate_schema

# ----

# TODO: Add support for input files;
# TODO: Add support for input strings with wildcards.
# TODO: Add support for launching applications within Singularity images.
# TODO: Add support for launching Singularity container applications.

# ----

# Define all available module properties.
__all__ = ["app_exec"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __check_exectype__(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function checks the application type (e.g., `serial` versus
    `multi` processor task allocations) and assigns the number of
    allotted tasks accordingly.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes with updated attributes with respect to
        the allocated task attributes.

    Raises
    ------

    ExecutableInterfaceError:

        - raised if the total number of tasks for a `multi` (e.g.,
          parallel) executable is zero.

    """

    # Determine the number of tasks/processors to allocate for the
    # respective application.
    if not any([exec_obj.multi, exec_obj.serial]):
        exec_obj.serial = True
    if exec_obj.multi:
        for item in exec_obj.task_keys:
            value = parser_interface.enviro_get(envvar=item)
            if value is not None:
                ntasks = value
                break
        if ntasks == 0:
            msg = (
                "For parallel/multi-processor applications, the total "
                "number of available tasks must be non-zero. Aborting!!!"
            )
            raise ExecutableInterfaceError(msg=msg)
    if exec_obj.serial:
        ntasks = 1
    exec_obj.ntasks = ntasks

    return exec_obj


# ----


def __check_sifimg__(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function validates (any) Singularity image attributes.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes with updated attributes with respect to
        the Singularity image attributes.

    Raises
    ------

    ExecutableInterfaceError:

        - raised if a Singularity image is passed but does not exist.

    """

    # Check that the Singularity container is valid.
    if not fileio_interface.fileexist(path=exec_obj.img_path):
        msg = (
            f"The Singularity container path {exec_obj.img_path} "
            f"does not exist. Aborting!!!"
        )
        raise ExecutableInterfaceError(msg=msg)
    try:
        simgexec = system_interface.app_path(app="singularity")
        cmd = [simgexec, "inspect", "--quiet", exec_obj.img_path]
        try:
            subprocess.run(
                cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
            )
            check = True
        except subprocess.CalledProcessError as errmsg:
            msg = (
                "Singularity application check yielded the following message:"
                f"\n\n{errmsg}\n\n"
                f"The Singularity container {exec_obj.img_path} will "
                "not be used for the requested executable application "
                f"{exec_obj.exec_path}."
            )
            logger.info(msg=msg)
            check = False
    except AttributeError:
        check = False
    exec_obj.container = check

    return exec_obj


# ----


def __get_cmd__(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function builds the `subprocess` command list.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        `subprocess` command list.

    """

    # Build the executable application `subprocess` command list.
    exec_obj = __get_nprocs_flag__(exec_obj=exec_obj)
    cmd = []
    if exec_obj.nprocs_flag is None:
        cmd += [f"{exec_obj.exec_path}"]
    else:
        cmd += [
            f"{exec_obj.launcher}",
            f"{exec_obj.nprocs_flag}",
            f"{exec_obj.ntasks}",
            f"{exec_obj.exec_path}",
        ]
    exec_obj.cmd = cmd

    return exec_obj


# ----


def __get_nprocs_flag__(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function defines the respective scheduler flag for specifying
    the `number of processors` for the respective application.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the `number of
        processors` flag for the respective scheduler type.

    """

    # Define the `number of processors` flag accordingly.
    if exec_obj.scheduler.lower() == "mpi":
        if exec_obj.multi:
            nprocs_flag = "-np"
        else:
            nprocs_flag = None
    elif exec_obj.scheduler.lower() == "slurm":
        if exec_obj.multi:
            nprocs_flag = "-n"
        else:
            nprocs_flag = None
    else:
        nprocs_flag = None
    exec_obj.nprocs_flag = nprocs_flag

    return exec_obj


# ----


@contextmanager
def __redirect__(exec_obj: SimpleNamespace) -> Generator[IO, IO, None]:
    """
    Description
    -----------

    This function is a `contextmanager` to redirect standard error and
    standard output to specified file paths.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Yields
    ------

    stderr, stdout: Tuple[IO, IO]

        A Python tuple containing file objects for the standard error
        and output, respectively.

    """

    # Define the standard error and output file objects.
    if exec_obj.stderr is None:
        exec_obj.stderr = os.path.join(exec_obj.run_path, "stderr.log")
        msg = f"Setting `stderr` path to {exec_obj.stderr}."
        logger.warn(msg=msg)
    if exec_obj.stdout is None:
        exec_obj.stdout = os.path.join(exec_obj.run_path, "stdout.log")
        msg = f"Setting `stdout` path to {exec_obj.stdout}."
        logger.warn(msg=msg)
    with open(exec_obj.stderr, "w", encoding="utf-8") as stderr, open(
        exec_obj.stdout, "w", encoding="utf-8"
    ) as stdout:
        yield (stderr, stderr)


# ----


def __launcher(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function determines the executable application launcher.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

         A Python SimpleNamespace object containing the executable
         application launcher attributes.

    """

    # Define the launcher application to run the respective
    # executable.
    if exec_obj.launcher is None:
        if exec_obj.scheduler is not None:
            if exec_obj.scheduler.lower() == "mpi":
                launcher = system_interface.app_path(app="mpirun")
            elif exec_obj.scheduler.lower() == "slurm":
                launcher = system_interface.app_path(app="srun")
            else:
                msg = (
                    f"The job scheduler type {exec_obj.scheduler.upper()} "
                    "is not recognized. Aborting!!!"
                )
                raise ExecutableInterfaceError(msg=msg)
        else:
            msg = (
                "The respective platform does not specify a scheduler; "
                "all compiled executables will be assumed serial."
            )
            logger.warn(msg=msg)
            launcher = None
        exec_obj.launcher = launcher

    return exec_obj


# ----


def __run(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function executes the run-time for the respective
    application.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    """

    # Launch the respective application.
    exec_obj = __get_cmd__(exec_obj=exec_obj)
    msg = f"Launching executable {exec_obj.exec_path} in path {exec_obj.run_path}."
    logger.info(msg=msg)
    with __redirect__(exec_obj=exec_obj) as (stderr, stdout):
        with fileio_interface.chdir(exec_obj.run_path):
            proc = subprocess.Popen(exec_obj.cmd, stderr=stderr, stdout=stdout)
            proc.wait()
            exec_obj.rc = proc.returncode
    if exec_obj.rc != 0:
        msg = (
            f"Executable {exec_obj.exec_path} failed with error code {exec_obj.rc}; "
            f"the error log is available at {exec_obj.stderr}. Aborting!!!"
        )
        raise ExecutableInterfaceError(msg=msg)
    msg = (
        f"Executable {exec_obj.exec_path} completed with return code {exec_obj.rc}.\n"
        f"Executable {exec_obj.exec_path} `stderr` written to path {exec_obj.stderr}\n."
        f"Executable {exec_obj.exec_path} `stdout` written to path {exec_obj.stdout}."
    )
    logger.info(msg=msg)

    return exec_obj


# ----


def __schema(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function defines the path to the YAML-formatted file
    containing the executable application schema.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes schema path.

    Raises
    ------

    ExecutableInterfaceError:

        - raised if an exception is raised while attempting to define
          the path to the YAML-formatted executable application schema
          file.

        - raised if the YAML-formatted executable application schema
          file does not exist.

    """

    # Define the path to the YAML-formatted schema file.
    try:
        schema_path = os.path.join(
            parser_interface.enviro_get(envvar="PYUTILS_ROOT"),
            "execute",
            "schema",
            "executable.schema.yaml",
        )
    except TypeError as errmsg:
        msg = (
            "Defining the executable schema path failed with error "
            f"`{errmsg}`; please check that the environment variable "
            f"`PYUTILS_ROOT` is defined within the run-time environment. "
            "Aborting!!!"
        )
        raise ExecutableInterfaceError(msg=msg) from errmsg
    if not fileio_interface.fileexist(path=schema_path):
        msg = (
            f"The YAML-formatted schema file path {schema_path} "
            "does not exist. Aborting!!!"
        )
        raise ExecutableInterfaceError(msg=msg)
    msg = f"Schema file is {schema_path}."
    logger.info(msg=msg)
    exec_obj.schema_path = schema_path

    return exec_obj


# ----


def __setup(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function initializes the Python SimpleNamespace object in
    accordance with both the executable application schema and the
    attributes specified upon entry.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes as specified by the executable
        application schema.

    """

    # Initialize the Python SimpleNamespace object.
    exec_dict = parser_interface.object_todict(object_in=exec_obj)
    cls_schema = build_schema(
        schema_def_dict=YAML().read_yaml(yaml_file=exec_obj.schema_path)
    )
    exec_dict = validate_schema(
        cls_schema=cls_schema, cls_opts=exec_dict, write_table=False
    )
    exec_obj = parser_interface.dict_toobject(in_dict=exec_dict)

    return exec_obj


# ----


def __validate(exec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function validates the schema for the respective executable
    application.

    Parameters
    ----------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application attributes.

    Returns
    -------

    exec_obj: SimpleNamespace

        A Python SimpleNamespace object containing the executable
        application schema defined attributes.

    """

    # Update the Python SimpleNamespace object accordingly.
    if (
        parser_interface.object_getattr(object_in=exec_obj, key="img_path", force=True)
        is not None
    ):
        exec_obj = __check_sifimg__(exec_obj=exec_obj)
    exec_obj = __check_exectype__(exec_obj=exec_obj)

    # Build the schema for the respective executable application.
    exec_dict = parser_interface.object_todict(object_in=exec_obj)
    cls_schema = build_schema(
        schema_def_dict=YAML().read_yaml(yaml_file=exec_obj.schema_path)
    )
    exec_dict = validate_schema(cls_schema=cls_schema, cls_opts=exec_dict)
    exec_obj = parser_interface.dict_toobject(in_dict=exec_dict)

    return exec_obj


# ----


def app_exec(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for an executable function.

    Parameters
    ----------

    func: Callable

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: Callable

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    async def wrapper_function(*args: Tuple, **kwargs: Dict) -> Callable:
        """
        Description
        -----------

        This method configures and runs the respective executable
        application.

        Other Parameters
        ----------------

        args: Tuple

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: Dict

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Configure and launch the respective executable application.
        if inspect.iscoroutinefunction(func):
            exec_obj = await func(*args, **kwargs)
        else:
            exec_obj = func(*args, **kwargs)
        exec_obj = __schema(exec_obj=exec_obj)
        exec_obj = __setup(exec_obj=exec_obj)
        exec_obj = __launcher(exec_obj=exec_obj)
        exec_obj = __validate(exec_obj=exec_obj)
        exec_obj = __run(exec_obj=exec_obj)

    return wrapper_function
