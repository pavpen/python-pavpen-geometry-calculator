"""Adds a documentation version selection control to the navigation side bar in
HTML pages

Overrides the `sidebar/variant-selector.html` template.

Does not support document names containing slashes, or back slashes.
"""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Final, cast

import docutils.nodes
import sphinx.environment
import sphinx.util.typing
from sphinx.application import Sphinx

__version__: Final[str] = "0.1.0"
_ENV_DATA_FORMAT: Final[str] = "0.1"
_DOC_VERSION_REG_EX: Final[re.Pattern[str]] = re.compile(r"v[\d]+([.][\d]+)*")

_DOC_NAME_TO_VERSION_EVENT_NAME: Final[str] = "doc-name-to-version"
"""Extracts the documentation version string from a Sphinx document name
"""

_DOC_NAME_TO_CROSS_VERSION_NAME: Final[str] = "doc-name-to-cross-version-name"
"""Converts a Sphinx document name (with a possible documentation version in
the path) to the name of the document across documentation versions

This allows linking a document to the same document in other documentation
versions.  E.g., if document `v0.1/api/algebra`, and `v0.2/api/algebra`
document different versions of the same API module, the cross-version name of
both `v0.1/api/algebra`, and `v0.2/api/algebra` may be `api/algebra`.
"""


@dataclass(frozen=True)
class VersionedDocName:
    cross_version_doc_name: str
    documentation_version: str


@dataclass(frozen=True)
class DocRevisionReference(VersionedDocName):
    doc_name: str
    relative_url: str


def default_doc_name_to_version(app: Sphinx, doc_name: str) -> str:
    """Default handler for the [_DOC_NAME_TO_VERSION_EVENT_NAME] event"""

    first_path_component = Path(doc_name).parts[0]

    if _DOC_VERSION_REG_EX.fullmatch(first_path_component) is not None:
        return first_path_component

    return app.config["version"]


def default_doc_name_to_cross_version_name(
    app: Sphinx,  # noqa: ARG001
    doc_name: str,
) -> str:
    """Default handler for the [_DOC_NAME_TO_CROSS_VERSION_NAME] event"""

    path = Path(doc_name)

    if _DOC_VERSION_REG_EX.fullmatch(path.parts[0]) is not None:
        # We don't support slashes, and back slashes in document names
        return "/".join(path.parts[1:])

    return doc_name


def _doc_name_to_version(app: Sphinx, doc_name: str) -> str:
    result = app.emit_firstresult(_DOC_NAME_TO_VERSION_EVENT_NAME, doc_name)
    if result is None:
        message = (
            f"Failed to resolve Sphinx document name ({doc_name!r}) to a "
            f"documentation version using the "
            f"{_DOC_NAME_TO_VERSION_EVENT_NAME!r} Sphinx event!"
        )
        raise ValueError(message)

    return result


def _doc_name_to_cross_version_name(app: Sphinx, doc_name: str) -> str:
    result = app.emit_firstresult(_DOC_NAME_TO_CROSS_VERSION_NAME, doc_name)
    if result is None:
        message = (
            f"Failed to resolve Sphinx document name ({doc_name!r}) to a "
            f"cross-documentation version name using the "
            f"{_DOC_NAME_TO_CROSS_VERSION_NAME!r} Sphinx event!"
        )
        raise ValueError(message)

    return result


def handle_doctree_resolved(app: Sphinx, doctree: docutils.nodes.document, docname: str) -> None:
    """Handles
    ["doctree-resolved"](https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#event-doctree-resolved)
    events for this extension
    """


def handle_env_udated(app: Sphinx, env: sphinx.environment.BuildEnvironment) -> Iterable[str]:
    """Handles
    ["env-updated"](https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#event-env-updated)
    events for this extension

    Currently, this includes building a list of documentation versions for
    hyper-linking.
    """

    versioned_doc_name_to_doc_name = {
        VersionedDocName(
            cross_version_doc_name=_doc_name_to_cross_version_name(app, doc_name),
            documentation_version=_doc_name_to_version(app, doc_name),
        ): doc_name
        for doc_name in env.found_docs
    }
    doc_versions = {versioned_doc_name.documentation_version for versioned_doc_name in versioned_doc_name_to_doc_name}

    env.versioned_doc_name_to_doc_name = versioned_doc_name_to_doc_name
    env.doc_versions = doc_versions

    return []


def handle_html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,  # noqa: ARG001
    context: dict[str, object],
    doctree: docutils.nodes.document | None,  # noqa: ARG001
) -> str | None:
    """Handles
    ["html-page-context"](https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#event-html-page-context)
    events for this extension
    """

    versioned_doc_name_to_doc_name = cast("dict[VersionedDocName, str]", app.env.versioned_doc_name_to_doc_name)
    doc_versions = cast("set[str]", app.env.doc_versions)
    cross_version_doc_name = _doc_name_to_cross_version_name(app=app, doc_name=pagename)
    documentation_version = _doc_name_to_version(app=app, doc_name=pagename)
    doc_name_revisions = [
        DocRevisionReference(
            cross_version_doc_name=cross_version_doc_name,
            documentation_version=version,
            doc_name=doc_name,
            relative_url=app.builder.get_relative_uri(from_=pagename, to=doc_name),
        )
        for version in doc_versions
        if (
            doc_name := versioned_doc_name_to_doc_name.get(
                VersionedDocName(cross_version_doc_name=cross_version_doc_name, documentation_version=version)
            )
        )
        is not None
    ]
    context["doc_name_revisions"] = doc_name_revisions
    context["doc_name_revision"] = DocRevisionReference(
        cross_version_doc_name=cross_version_doc_name,
        documentation_version=documentation_version,
        doc_name=pagename,
        relative_url="",
    )
    context["current_version"] = documentation_version


def setup(app: Sphinx) -> sphinx.util.typing.ExtensionMetadata:
    """Initializes the Sphinx extension, registering nodes, directives, events,
    etc.

    See
    [§The `setup` function](https://www.sphinx-doc.org/en/master/development/tutorials/extending_syntax.html#the-setup-function)
    in the
    [Extending syntax with roles and directives](https://www.sphinx-doc.org/en/master/development/tutorials/extending_syntax.html#extending-syntax-with-roles-and-directives)
    Sphinx tutorial.
    """

    # Add a CSS file to HTML output:
    # * https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_css_file
    #
    # Nodes re-processed after the full document tree:
    # * https://docutils.sourceforge.io/docs/howto/rst-directives.html#toc-entry-8

    # TODO(pavel.penev): Find a more reliably way to override a template, which
    #   can be shared across themes.
    #
    #   Add template overrides.  This has poor reliability.  The order of
    # extension can matter, if multiple extension override the same template.
    extension_dir = Path(__file__).parent
    template_dir = extension_dir / "templates"
    app.config.templates_path.append(str(template_dir))

    app.add_event(_DOC_NAME_TO_VERSION_EVENT_NAME)
    app.connect(_DOC_NAME_TO_VERSION_EVENT_NAME, default_doc_name_to_version)
    app.add_event(_DOC_NAME_TO_CROSS_VERSION_NAME)
    app.connect(_DOC_NAME_TO_CROSS_VERSION_NAME, default_doc_name_to_cross_version_name)

    app.connect("env-updated", handle_env_udated)
    app.connect("doctree-resolved", handle_doctree_resolved)
    app.connect("html-page-context", handle_html_page_context)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
