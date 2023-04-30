# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "localized-unidecode"
copyright = "2023, Kristupas Talačka"
author = "Kristupas Talačka"

import tomli

version = tomli.load(open("../pyproject.toml", "rb"))["project"]["version"]

# package location
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

import mock

MOCK_MODULES = ["pycountry", "unidecode"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()
