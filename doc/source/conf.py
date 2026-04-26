# noqa: INP001 # This file doesn't need to be part of a Python package

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import enum
import inspect
import itertools
import subprocess
import sys
import tomllib
import warnings
from collections.abc import Iterable
from pathlib import Path
from typing import Final, TypeVar, cast

import sphinx.addnodes
import sphinx.domains
from sphinx.application import Sphinx

GIT_PATH: Final[str] = "git"


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


project_path = Path(__file__).parent.parent.parent

# Parse <../../pyproject.toml>, so we can re-use values from it.
with open(project_path / "pyproject.toml", "rb") as pyproject_file:
    pyproject_dict = tomllib.load(pyproject_file)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Geometry Calculator"
author = ",".join(author["name"] for author in pyproject_dict["project"]["authors"])
copyright = f"2026, {author}"  # noqa: A001
release = get_version()

# Extract the <major.minor> part of `release`:
version = ".".join(release.split(".")[:2])

license_name = pyproject_dict["project"]["license"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

needs_sphinx = "1.3"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
]
needs_extensions = {
    "sphinx.ext.autodoc": "1.1",
}

# Extension configuration
autosummary_generate = True  # Enable `sphinx.ext.autosummary`.

# Generate documentation for imported symbols:
autosummary_imported_members = True

# Base URLs for links to external packages
# <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#module-sphinx.ext.intersphinx>:
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# -- Internationalisation ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalisation

language = "en"

# -- Markup ------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-markup

trim_footnote_reference_space = True

# -- Nitpicky Mode (i.e., Reference, and Link Validation) --------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-nitpicky-mode

nitpicky = True

# -- Object Signatures (i.e., Programming Symbol Rendering) ------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-object-signatures

toc_object_entries = True

# -- Source Files ------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-source-files

exclude_patterns = []

# -- Templating --------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-templating

# Override templates:
templates_path = ["theme-overrides/templates"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# TODO(pavel.penev): Replace with https://github.com/jbms/sphinx-immaterial/
#     when it becomes stable
#
# Borrow the Python documentation theme
# <https://github.com/python/python-docs-theme>:
html_theme = "furo"
html_theme_options: dict[str, object] = {}
html_theme_path = ["theme-overrides"]

# Custom theme variables passed to templates:
html_context = {"license_name": license_name}

html_favicon = None
html_static_path = ["_static"]

#
# Plug-in code configuration
#
source_url = pyproject_dict["project"]["urls"]["Source"].removesuffix("/")
is_repository_dirty_command = subprocess.run(
    [GIT_PATH, "status", "--porcelain"], shell=False, check=True, capture_output=True, encoding="utf-8"
)
is_repository_dirty = is_repository_dirty_command.stdout.strip() != ""
if is_repository_dirty:
    warnings.warn(
        RuntimeWarning(
            f"Current repository is dirty!  Links to documentation source code "
            f"may be invalid: {is_repository_dirty_command.args} output: "
            f"stdout: {is_repository_dirty_command.stdout} "
            f"stderr: {is_repository_dirty_command.stderr}"
        ),
        stacklevel=1,
    )
long_commit_id = subprocess.run(
    [GIT_PATH, "rev-parse", "HEAD"], shell=False, check=True, capture_output=True, encoding="utf-8"
).stdout.rstrip()


def get_symbol_in_module(module: object, symbol_name: str) -> object:
    result = module
    for name_component in symbol_name.split("."):
        result = getattr(result, name_component)

    return result


def linkcode_resolve(domain: str, info: dict[str, str]) -> str | None:
    """Returns the URL corresponding to a code symbol for links to source code
    in the documentation

    * Called by the `sphinx.ext.linkcode` extension.  See
      <https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html#configuration>.

    Links to properties, enums, and variables are not supported.  They're
    replaced with links to the parent supported symbol, such as the containing
    class, or module.
    """

    if domain != "py":
        message = f"Unsupported Sphinx domain: {domain!r}"
        raise ValueError(message)

    module_name = info["module"]
    if len(module_name) < 0:
        message = f"Symbol with no module: {info!r}"
        raise ValueError(message)
    symbol_name = info["fullname"]

    module = sys.modules[module_name]
    symbol = get_symbol_in_module(module, symbol_name)
    # TODO(pavel.penev): Switch to using `ast` for obtating the line numbers,
    #     of symbol definitions.
    if isinstance(symbol, property):
        # `inspect.source_path` doesn't support properties, we link to the
        # class containing the property instead:
        [parent_symbol_name, _] = symbol_name.rsplit(".", maxsplit=1)
        symbol = get_symbol_in_module(module, parent_symbol_name)
    if isinstance(symbol, enum.EnumType) or isinstance(symbol.__class__, enum.EnumType):
        # `inspect.source_path` doesn't support enum classes, or constanets, we
        # link to the containing module instead:
        symbol = module
    if (
        not inspect.ismodule(symbol)
        and not inspect.isclass(symbol)
        and not inspect.ismethod(symbol)
        and not inspect.isfunction(symbol)
        and not inspect.istraceback(symbol)
        and not inspect.isframe(symbol)
        and not inspect.iscode(symbol)
    ):
        # We may have obtained the value of the symbol, rather than an object
        # that can give us information about the symbol definiton.  Link to the
        # containing symbol instead:
        symbol_name_components = symbol_name.rsplit(".", maxsplit=1)
        if len(symbol_name_components) < 2:  # noqa: PLR2004
            symbol = module
        else:
            [parent_symbol_name, _] = symbol_name_components
            symbol = get_symbol_in_module(module, parent_symbol_name)
    relative_source_path = Path(inspect.getsourcefile(symbol)).relative_to(project_path)
    (source_lines, start_line_number) = inspect.getsourcelines(symbol)
    start_line_number = max(start_line_number, 1)
    end_line_number = start_line_number + len(source_lines) - 1

    return (
        f"{source_url}/blob/{long_commit_id}/{relative_source_path.as_posix()}#L{start_line_number}-L{end_line_number}"
    )


#
# Work-arounds for Sphinx bugs, and missing features
#
def get_class_generic_parameters(class_obj: object) -> Iterable[TypeVar]:
    try:
        return cast("tuple[TypeVar, ...]", class_obj.__parameters__)
    except AttributeError:
        return []


def get_module_generic_parameters(module_obj: object) -> Iterable[TypeVar]:
    return itertools.chain.from_iterable(
        get_class_generic_parameters(module_member)
        for module_member in vars(module_obj).values()
        if inspect.isclass(module_member)
    )


def get_class_qualified_name(class_obj: object) -> str:
    module_name = class_obj.__module__
    module_name_prefix = "" if module_name == "builtins" else f"{module_name}."

    return f"{module_name_prefix}{class_obj.__name__}"


def handle_autodoc_process_signature_adding_class_generic_parameters(
    app: Sphinx,  # noqa: ARG001
    obj_type: str,
    name: str,
    obj: object,  # noqa: ARG001
    options: object,  # noqa: ARG001
    signature: str | None,
    return_annotation: str,
) -> tuple[str | None, str]:
    """Handles an
    ["autodoc-process-signature" Sphinx autodoc event](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-process-signature)

    Provides a partial work-around implementation for
    [autodoc for generic classes should include the type parameters #10568](https://github.com/sphinx-doc/sphinx/issues/10568)

    Generic parameter bounds, and contraints in function, method, and class
    signatures, are not fixed.
    """

    def format_generic_parameter_suffix(generic_parameter: TypeVar) -> str:
        result = ""

        constraints = generic_parameter.__constraints__
        if len(constraints) > 0:
            result += f": {tuple(str(c) for c in constraints)}"

        bound = generic_parameter.__bound__
        if bound is not None:
            result += f": {bound}"

        return result

    def format_generic_parameter(generic_parameter: TypeVar) -> str:
        return f"{generic_parameter}{format_generic_parameter_suffix(generic_parameter)}"

    if obj_type == "class":
        [module_name, class_name] = name.rsplit(".", maxsplit=1)
        generic_parameter_list = ", ".join(
            format_generic_parameter(parameter)
            for parameter in get_class_generic_parameters(getattr(sys.modules[module_name], class_name))
        )
        if len(generic_parameter_list) > 0:
            signature = f"[{generic_parameter_list}]{signature or ''}"

    return (signature, return_annotation)


def handle_warn_missing_reference_to_generic_parameter(
    app: Sphinx,  # noqa: ARG001
    domain: sphinx.domains.Domain,
    node: sphinx.addnodes.pending_xref,
) -> bool | None:
    """Handles a
    ["warn-missing-reference" Sphinx event](https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#event-warn-missing-reference)

    Fixes:

    ```
    <unknown>:1: WARNING: py:class reference target not found: Vector [ref.class]
    <unknown>:5: WARNING: py:obj reference target not found: typing.Vector [ref.obj]
    ```

    and

    ```
    <unknown>:1: WARNING: py:class reference target not found: Scalar [ref.class]
    ```

    which seem to be due to
    [Use of TypeVar results in "reference target not found" error #10974](https://github.com/sphinx-doc/sphinx/issues/10974).
    """

    if domain.name != "py":
        return
    reftarget = cast("str | None", node.get("reftarget", None))
    reftype = cast("str | None", node.get("reftype", None))
    if reftarget is not None:
        py_class_name = cast("str | None", node.get("py:class"))
        py_module_name = cast("str | None", node.get("py:module"))
        if py_module_name is not None and reftype in ("class", "obj"):
            if py_class_name is None:
                generic_parameters = get_module_generic_parameters(sys.modules[py_module_name])
            else:
                generic_parameters = get_class_generic_parameters(getattr(sys.modules[py_module_name], py_class_name))
            referenced_symbol_name = reftarget.removeprefix("typing.")
            if referenced_symbol_name in (str(p) for p in generic_parameters):
                # This "missing-reference" is to a generic type parameter.
                # Ignore it:
                return True

    return None


def setup(app: Sphinx):
    app.connect("autodoc-process-signature", handle_autodoc_process_signature_adding_class_generic_parameters)
    app.connect("warn-missing-reference", handle_warn_missing_reference_to_generic_parameter)
