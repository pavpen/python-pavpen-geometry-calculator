from collections.abc import Callable, Sequence
from typing import ClassVar

import docutils.nodes
import sphinx.util.docutils
import sphinx.writers.html5
from sphinx.application import Sphinx


class MenuItemNode(docutils.nodes.General, docutils.nodes.Inline, docutils.nodes.Element):
    """Stores in an item in a [SelectNode] list of selectable options

    See [SelectNode].
    """

    content_model = ((docutils.nodes.Body, "+"),)  # (%body.elements;)+


class SelectNode(docutils.nodes.General, docutils.nodes.Inline, docutils.nodes.Element):
    """Stores a list of selectable options, usually rendered as drop-down menu

    A `docutils` node class cannot be defined in a `conf.py`.  If you try,
    you'll currently encounter an error thay may look like:

    ```
      File ".../doc/Lib/site-packages/sphinx/builders/__init__.py", line 696, in write_doctree
        pickle.dump(doctree, f, pickle.HIGHEST_PROTOCOL)
        ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    _pickle.PicklingError: Can't pickle <class 'SelectNode'>: it's not found as builtins.SelectNode
    when serializing SelectNode class
    when serializing SelectNode object
    when serializing list item 1
    when serializing dict item 'children'
    when serializing docutils.nodes.section state
    when serializing docutils.nodes.section object
    when serializing list item 1
    when serializing dict item 'children'
    when serializing docutils.nodes.document state
    when serializing docutils.nodes.document object
    ```

    See:
    * [Custom Sphinx directive gives a pickling error](https://stackoverflow.com/questions/69363905/custom-sphinx-directive-gives-a-pickling-error)
    * [[docs][ext] Emphasise that one shouldn't put their node child classes in conf.py #6751](https://github.com/sphinx-doc/sphinx/issues/6751)
    * [Trying to follow "Tutorial: Writing a simple extension" leads to PicklingError #1493](https://github.com/sphinx-doc/sphinx/issues/1493)
    * [PicklingError on environment when config option value is a callable #1424](https://github.com/sphinx-doc/sphinx/issues/1424)
    """

    content_model = ((MenuItemNode, "+"),)  # (%menu-item.elements;)+


def _validate_doctree_node(node: docutils.nodes.Element):
    try:
        node.validate_content()
    except docutils.nodes.ValidationError as e:
        source_line_number = node.line
        line_number_suffix = "" if source_line_number is None else f":{source_line_number}"
        e.add_note(
            f"While processing docutils node defined {'in' if len(line_number_suffix) < 1 else 'on'} {node.source}{line_number_suffix}"
        )
        raise


class MenuItemNodeHtmlWriter:
    @staticmethod
    def visit(translator: sphinx.writers.html5.HTML5Translator, node: MenuItemNode) -> None:
        _validate_doctree_node(node)

        attributes: dict[str, str] = {}

        value = node.get("value", None)
        if value is not None:
            attributes["value"] = value

        label = node.get("label", None)
        if label is not None:
            attributes["label"] = label

        translator.body.append(translator.starttag(node=node, tagname="option", empty=False, **attributes))

    @staticmethod
    def leave(
        translator: sphinx.writers.html5.HTML5Translator,
        node: MenuItemNode,  # noqa: ARG004
    ) -> None:
        translator.body.append("</option>\n")

    @staticmethod
    def get_visitor_handlers() -> tuple[
        Callable[[sphinx.writers.html5.HTML5Translator, MenuItemNode], None],
        Callable[[sphinx.writers.html5.HTML5Translator, MenuItemNode], None],
    ]:
        return (MenuItemNodeHtmlWriter.visit, MenuItemNodeHtmlWriter.leave)


class SelectNodeHtmlWriter:
    @staticmethod
    def visit(translator: sphinx.writers.html5.HTML5Translator, node: SelectNode) -> None:
        _validate_doctree_node(node)

        translator.body.append(translator.starttag(node=node, tagname="select"))

    @staticmethod
    def leave(
        translator: sphinx.writers.html5.HTML5Translator,
        node: SelectNode,  # noqa: ARG004
    ) -> None:
        translator.body.append("</select>\n")

    @staticmethod
    def get_visitor_handlers() -> tuple[
        Callable[[sphinx.writers.html5.HTML5Translator, SelectNode], None],
        Callable[[sphinx.writers.html5.HTML5Translator, SelectNode], None],
    ]:
        return (SelectNodeHtmlWriter.visit, SelectNodeHtmlWriter.leave)


class SelectDirective(sphinx.util.docutils.SphinxDirective):
    name = "select"
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[dict[str, Callable[[str], object]] | None] = {}
    has_content = True

    def run(self) -> Sequence[docutils.nodes.Node]:
        self.assert_has_content()
        content_nodes = self.parse_content_to_nodes()
        content_string = "\n".join(self.content)

        result = SelectNode()
        result.extend(content_nodes)
        result.rawsource = content_string
        return [result]


class MenuItemDirective(sphinx.util.docutils.SphinxDirective):
    name = "menu-item"
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[dict[str, Callable[[str], object]] | None] = {}
    has_content = True

    def run(self):
        self.assert_has_content()
        content_nodes = self.parse_content_to_nodes()
        content_string = "\n".join(self.content)

        result = MenuItemNode()
        result.extend(content_nodes)
        result.rawsource = content_string
        return [result]


def setup(app: Sphinx):
    """Initializes the Sphinx extension, registering nodes, directives, events,
    etc.
    """

    # Add a doctree node:
    # * https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_node
    #
    # Add a ReStructuredText directive:
    # * https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_directive
    # * https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_directive_to_domain
    #
    # Add a CSS file to HTML output:
    # * https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_css_file
    #
    # Nodes re-processed after the full document tree:
    # * https://docutils.sourceforge.io/docs/howto/rst-directives.html#toc-entry-8
    app.add_node(MenuItemNode, html=MenuItemNodeHtmlWriter.get_visitor_handlers())
    app.add_node(SelectNode, html=SelectNodeHtmlWriter.get_visitor_handlers())
    app.add_directive(SelectDirective.name, SelectDirective)
    app.add_directive(MenuItemDirective.name, MenuItemDirective)
