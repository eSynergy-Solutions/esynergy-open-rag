# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Open RAG"
copyright = "2024, Adrian Gonzalez"
author = "Adrian Gonzalez"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]
# Display ToDos by setting to true
todo_include_todos = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_mock_imports = ["altair.vegalite.v4"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 1}
html_static_path = ["_static"]
