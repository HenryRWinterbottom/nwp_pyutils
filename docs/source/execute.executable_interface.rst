executable_interface
====================

.. currentmodule:: execute.executable_interface

.. autofunction:: app_exec

-----------------
Schema Attributes
-----------------

The following are the mandatory Python `SimpleNamespace` schema attributes.

.. list-table::
   :widths: auto
   :header-rows: 1
   :align: left

   * - **Attribute**
     - **Description**
     - **Type**
   * - ``exec_path``
     - The directory tree path for the respective executable
       application.
     - ``str``
   * - ``run_path``
     - The directory tree path where the respective executable
       application is to be executed.
     - ``str``

The following are the `SimpleNamespace` schema attributes describing
the executable application.

.. list-table::
   :widths: auto
   :header-rows: 1
   :align: left

   * - **Attribute**
     - **Description**
     - **Type**
     - **Default**
   * - ``multi``
     - Boolean value indicating that the executable application is a
       multiple CPU-type executable.
     - ``bool``
     - ``False``; if ``False``, ``serial`` (below) will be set to
       ``True`` by default.
   * - ``serial``
     - Boolean value indicating that the executable application is a
       serial-type executable.
     - ``bool``
     - ``False``; set to ``True`` if ``multi`` (above) is ``False``.
   * - ``stderr``
     - The directory tree path for the executable application standard
       error.
     - ``str``
     - If not specified, the standard error will be written to the
       directory tree path for the respective executable application
       within the file ``stderr.log``.
   * - ``stdin``
     - An ordered list of inputs for the respective executable
       application.
     - ``list``
     -
   * - ``stdout``
     - The directory tree path for the executable application standard
       output.
     - ``str``
     - If not specified, the standard output will be written to the
       directory tree path for the respective executable application
       within the file ``stdout.log``.
