from __future__ import annotations
from .tree_sitter_base import TreeSitterParser


class JavaParser(TreeSitterParser):
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

        identifiers = []

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
        elif node.type in (
            "field_declaration",
            "local_variable_declaration",
        ):
            identifiers += self.get_identifiers_from_field_declaration(
                node,
                src_lines,
            )
        else:
            # these node types are more generic and the identifiers can all be
            # extracted from a child node
            child_type = ""

            # if node.type == "superclass":
            #     child_type = "type_identifier"

            if node.type in (
                "class_declaration",
                "enum_declaration",
                "method_declaration",
                "interface_declaration",
                "formal_parameter",  # function arguments
            ):
                child_type = "identifier"

            # elif node.type == "import_declaration":
            #     # package imports
            #     child_type = "scoped_identifier"

            if child_type != "":
                identifiers.append(
                    self.get_identifier_from_child(
                        node,
                        src_lines,
                        child_type,
                    )
                )

        if len(identifiers) > 0:
            for identifier in identifiers:
                # non-compiling code may return empty strings or None
                if identifier != "" and identifier is not None:
                    parsed_file.add_code_identifier(identifier)

    def get_identifiers_from_field_declaration(self, node, src_lines) -> str:
        """ add identifiers """
        identifiers = []
        for child in node.children:
            if child.type == "variable_declarator":
                identifiers.append(
                    self.get_identifier_from_child(
                        node=child,
                        src_lines=src_lines,
                        child_type="identifier",
                    )
                )
        return identifiers
