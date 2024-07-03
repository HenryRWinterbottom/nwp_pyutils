#!/usr/bin/env python3

"""
Script
------

    conf.py

Description
-----------

    This script is the driver script for configuring the
    `sphinx-build` runtime environment in order to build the
    respective API.

Author(s)
---------

    Henry R. Winterbottom; 15 October 2023

History
-------

    2023-10-15: Henry Winterbottom -- Initial implementation.

"""

# ----

import sys
import os
sys.path.insert(0, os.path.abspath("../../"))

# ----


def setup(app):
    app.add_css_file("custom.css")
    app.add_css_file("theme_overrides.css")

# ----


# Project information.
project = "UFS Python Utilities"
copyright = "2023 Henry R. Winterbottom"
author = "2023 Henry R. Winterbottom"
# release = None

# General configuration.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "numpydoc",
    "sphinx_autodoc_typehints",
    "readthedocs_ext.readthedocs",
]
exclude_patterns = []
source_suffix = ".rst"
master_doc = "index"

# API attributes.
autoapi_dirs = [
    "../../confs",
    "../../ioapps",
    "../../tools",
    "../../utils",
]
autoapi_type = "python"
autoapi_ignore = ["*test_*_interface*.py*", "*tests*", "*namelist*"]

# Options for HTML output.
pygments_style = "sphinx"
html_theme = "furo"
html_theme_path = ["_themes"]
html_theme_options = {"body_max_width": "none"}
html_static_path = []
html_context = {}
htmlhelp_basename = "ufs_pyutils"
