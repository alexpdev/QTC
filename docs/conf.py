#!/usr/bin/env python
#
# qtc documentation build configuration file, created by
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import Qtc

# -- General configuration ---------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.md'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Qtc'
copyright = "2020, AlexpDev"
author = "AlexpDev"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = Qtc.__version__
# The full version, including alpha/beta/rc tags.
release = Qtc.__version__

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '__settings.py']

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
