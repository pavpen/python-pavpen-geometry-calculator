# noqa: INP001 # This file doesn't need to be part of a Python package

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import tomllib
from pathlib import Path


def get_version() -> str:
    # The `.. autosummary::` directive from the `sphinx.ext.autodoc` extension
    # from Sphinx 9.1.0 fails, if the module in the `autosumary` is imported in
    # the global namespace.  Therefore, we import it in a limeted scope here,
    # and delet the reference after use.
    #   The failure exception looks like:
    # Traceback (most recent call last):
    #   File "...\Lib\site-packages\sphinx\ext\autodoc\_dynamic\_importer.py", line 131, in _import_from_module_and_path
    #     module = _import_module(module_name, try_reload=True)
    #   File "...\Lib\site-packages\sphinx\ext\autodoc\_dynamic\_importer.py", line 218, in _import_module
    #     raise ModuleNotFoundError(msg, name=modname)
    #     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # ModuleNotFoundError: No module named 'geometry_calculator'
    #  [autodoc.import_object]
    import pavpen.geometry_calculator  # noqa: PLC0415

    result = pavpen.geometry_calculator.__version__
    del pavpen.geometry_calculator

    return result


# Parse <../../pyproject.toml>, so we can re-use values from it.
with open(Path(__file__).parent.parent.parent / "pyproject.toml", "rb") as pyproject_file:
    pyproject_dict = tomllib.load(pyproject_file)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Geometry Calculator"
release = get_version()
author = ",".join(author["name"] for author in pyproject_dict["project"]["authors"])
copyright = f"2026, {author}"  # noqa: A001

license_name = pyproject_dict["project"]["license"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ["_templates"]
exclude_patterns = []

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
]
autosummary_generate = True  # Enable `sphinx.ext.autosummary`.


# Base URLs for links to external packages
# <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#module-sphinx.ext.intersphinx>:
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Borrow the Python documentation theme
# <https://github.com/python/python-docs-theme>:
html_theme = "python_docs_theme"
html_favicon = None
html_static_path = ["_static"]
html_theme_path = ["theme-overrides"]

# HTML override templates:
templates_path = ["theme-overrides/templates"]

html_theme_options: dict[str, object] = {
    "collapsiblesidebar": True,
    "issues_url": pyproject_dict["project"]["urls"]["Issues"],
    "license_url": "/license.html",
    "root_url": pyproject_dict["project"]["urls"]["Source"],
    "root_name": project,
    "root_icon": None,
    "root_include_title": False,  # We use the version switcher instead.
}

# Custom theme variables passed to override templates:
html_context = {"license_name": license_name}
