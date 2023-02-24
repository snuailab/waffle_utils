# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Waffle Utils 🥛'
copyright = '2023, huijae lee'
author = 'huijae lee'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Custom Options ----------------------------------------------------------


import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']

templates_path = ['_templates']
