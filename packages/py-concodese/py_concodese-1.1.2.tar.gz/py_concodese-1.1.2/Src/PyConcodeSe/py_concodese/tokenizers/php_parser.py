from __future__ import annotations
from .tree_sitter_base import TreeSitterParser


class PhpParser(TreeSitterParser):
    def __init__(self, grammar_path) -> None:
        super().__init__(
            language="php",
            extension=".php",
            grammar_path=grammar_path,
        )

    def process_node(self, node, parsed_file, src_lines) -> None:
        """
        updates the parsed_file object if this node contains a comment or
        identifier of interest
        """
        identifiers = []

        # handle the node according to its type
        if node.type == "namespace_definition":
            # set the package of the parsed file
            parsed_file.set_package(
                self.get_identifier_from_child(
                    node,
                    src_lines,
                    "namespace_name",
                )
            )
        elif node.type == "comment":
            comment = self.process_substring(
                src_lines, node.start_point, node.end_point
            )
            parsed_file.add_comment_string(comment)
            return  # no code identifiers in comment nodes
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
                "function_definition",
                "variable_name",
                "simple_parameter",
                "class_declaration",
                "class_interface_clause",
                "use_declaration",
                "method_declaration",
                "formal_parameter",  # function arguments
            ):
                # child_type = "identifier"
                child_type = "name"

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
