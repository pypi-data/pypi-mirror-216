from __future__ import annotations
from .tree_sitter_base import TreeSitterParser


class JavaParserSupplementary(TreeSitterParser):
    """This parser only stores comments, package and file info.
    The majority of identifiers are ignored.
    It parses for data to supplement Jim data with.
    Jim will already extract all the identifiers and create tokens.
    """

    def __init__(self, grammar_path) -> None:
        super().__init__(
            language="java",
            extension=".java",
            grammar_path=grammar_path,
        )

    def process_node(self, node, parsed_file, src_lines) -> None:
        """
        updates the parsed_file object if this node contains a comment or
        identifier of interest
        """
        if node.type == "comment":
            comment = self.process_substring(
                src_lines, node.start_point, node.end_point
            )
            parsed_file.add_comment_string(comment)
            return  # no code identifiers in comment nodes

        # handle the node according to its type
        if node.type == "package_declaration":
            # set the package of the parsed file
            parsed_file.set_package(
                self.get_identifier_from_child(
                    node,
                    src_lines,
                    "scoped_identifier",
                )
            )
