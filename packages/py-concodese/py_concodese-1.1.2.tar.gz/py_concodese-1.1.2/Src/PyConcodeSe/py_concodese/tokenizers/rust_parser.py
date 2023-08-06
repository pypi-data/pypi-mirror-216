from __future__ import annotations
from .tree_sitter_base import TreeSitterParser


class RustParser(TreeSitterParser):
    def __init__(self, grammar_path) -> None:
        super().__init__(
            language="rust",
            extension=".rs",
            grammar_path=grammar_path,
        )

    def process_node(self, node, parsed_file, src_lines) -> None:
        identifiers = []

        # handle the node according to its type
        if node.type == "use_declaration":
            # set the package of the parsed file
            parsed_file.set_package(self.get_identifier_from_child(node, src_lines, "scoped_identifier"))

        elif node.type == "identifier":
            identifiers.append(TreeSitterParser.try_decode(node.text))

        elif node.type == "line_comment":
            comment = self.process_substring(src_lines, node.start_point, node.end_point)
            parsed_file.add_comment_string(comment)
            return  # no code identifiers in comment nodes

        elif node.type in ("function_item", "let_declaration", "array_type"):  # get functions name
            identifiers.append(self.get_identifier_from_child(node, src_lines, child_type="identifier"))

        elif node.type in ("struct_item", "enum_item"):
            identifiers.append(self.get_identifier_from_child(node, src_lines, child_type="type_identifier"))

        else:
            if node.type in ("parameters", "string_literal", "parameters", "expression_statement"):
                identifiers.append(self.get_identifier_from_child(node, src_lines, child_type="identifier"))

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
