# SPDX-FileCopyrightText: 2022 The meson-python developers
#
# SPDX-License-Identifier: MIT

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import mesonpy


# -- Project information -----------------------------------------------------

project = 'meson-python'
copyright = '2021, The meson-python developers'

# The short X.Y version
version = mesonpy.__version__
# The full version, including alpha/beta/rc tags
release = mesonpy.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_autodoc_typehints',
    'sphinx_contributors',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxcontrib.spelling',
    'sphinxext.opengraph',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'importlib_resources': ('https://importlib-resources.readthedocs.io/en/latest/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

default_role = 'any'

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_title = f'meson-python {version}'

html_static_path = ['static']
html_css_files = [
    'css/contributors.css',
]

html_theme_options = {
    'light_css_variables': {
        'font-stack': (
            'system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,'
            'Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji'
        ),
    },
}


# Spellchecking

spelling_show_suggestions = True
spelling_warning = True


# Open Graph

ogp_site_url = 'https://meson-python.readthedocs.io'
ogp_site_name = 'meson-python documentation'


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
# html_static_path = ['_static']

autoclass_content = 'both'
