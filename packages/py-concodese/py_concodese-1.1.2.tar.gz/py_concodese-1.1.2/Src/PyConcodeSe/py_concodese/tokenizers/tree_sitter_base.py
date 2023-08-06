"""
This is subtly different in places from the original groovy tokenizer,
which was intentionally structured similar to the original java implementation.
Though this is unpythonic in structure, it does make comparisons to the original
groovy tokenizer from j-concodese easier.
"""

from __future__ import annotations
import logging
import os
from pathlib import Path
from tree_sitter import Language, Parser
from .parsed_file import ParsedFile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TreeSitterParser:
    """
    base class for parsers that use tree sitter
    sub classes should implement a 'process_node' function
    """

    def __init__(self, language, extension, grammar_path) -> None:
        """
        language - str that matches tree sitter language grammar folder
        extension - str or tuple of file extensions this tokenizer will parse
        grammar_path - str of path to the grammer root folder
        """
        build_path = os.path.join(grammar_path, f"build/{language}.so")

        Language.build_library(
            # Store the library in the `build` directory
            build_path,
            # Include one or more languages
            [
                os.path.join(grammar_path, f"tree-sitter-{language}-master"),
            ],
        )

        self.parser = Parser()

        self.extension = extension

        assert self.extension is not None
        self.parser.set_language(Language(build_path, language))

    def perform_extraction(self, project_path) -> list[ParsedFile]:
        """accept a single project path (dir) and processes all files in subfolders

        returns a list of ParsedFile instances"""
        paths_to_process = []
        paths_to_process += TreeSitterParser.list_files_for_folder(
            project_path, self.extension
        )

        parsed_files = []
        for idx, path_to_process in enumerate(paths_to_process):
            if (idx + 1) % 100 == 0:
                logger.info(f"parsing files {idx + 1}/{len(paths_to_process)}")

            parsed_files.append(
                self.parse_file_content(
                    path_to_process, path_to_process.replace(project_path, "")
                )
            )

        return parsed_files

    def parse_file_content(self, full_file_path, relative_path) -> ParsedFile:
        """parse a single src file and return a ParsedFile instance"""
        parsed_file = ParsedFile(
            file_name=Path(full_file_path).stem,
            extension=Path(full_file_path).suffix,
            relative_file_path=relative_path,
        )

        with open(full_file_path, "rb") as f:
            file_txt = f.read()
            src_lines = file_txt.splitlines()

            file_txt = b"\n".join(src_lines)

            tree = self.parser.parse(file_txt)
            tree_cursor = tree.walk()

            fully_parsed = False

            while not fully_parsed:
                # process each new node on arrival
                self.process_node(tree_cursor.node, parsed_file, src_lines)
                # try to get to child node
                if tree_cursor.goto_first_child():
                    continue
                # if no children go to next sibling, or move up tree until a sibling
                # is found
                while not tree_cursor.goto_next_sibling():
                    if not tree_cursor.goto_parent():
                        fully_parsed = True  # no remaining unprocessed nodes
                        break

        return parsed_file

    def get_identifier_from_child(self, node, src_lines, child_type):
        """returns single matching identifier"""
        for child in node.children:
            if child.type == child_type:
                return self.process_substring(
                    src_lines, child.start_point, child.end_point
                )

    def process_substring(self, src_lines, start_point, end_point) -> str:
        """returns a string from the file currently in processing
        start and end point follow the same format as the properties
        of tree sitter nodes of the same name.
        tuple(line_number,column_number)  (0 based indexes)
        """
        # assert an error if identifiers are ever split across lines
        line_idx = start_point[0]
        final_line_idx = end_point[0]

        substring = ""
        # start by adding all the complete lines into one string
        while line_idx < final_line_idx:
            # new line characters are removed but we want to ensure that lines
            # have at least a space between them.
            # decode each line individually in case of a decode error - then
            # the error will only affect a single line, not the whole string
            substring += self.try_decode(src_lines[line_idx])
            substring += " "
            line_idx += 1

        # add the final truncated line
        col_start = start_point[1]
        col_end = end_point[1]

        substring += self.try_decode(src_lines[line_idx][col_start:col_end])
        return substring

    @staticmethod
    def try_decode(byte_string) -> str:
        """decodes a byte string and returns the result.
        if string cannot be decoded, an error message is output
        and an empty string is returned
        """
        try:
            return byte_string.decode("utf-8")
        except UnicodeDecodeError:
            print(
                f"(result: attempting latin-1 decode) UTF-8 decode error occured on the line: {byte_string}"
            )
        try:
            return byte_string.decode("latin-1")
        except UnicodeDecodeError:
            print(
                f"(result: line skipped) latin-1 decode error occured on the line: {byte_string}"
            )
        return ""

    @staticmethod
    def list_files_for_folder(path, extension) -> list[str]:
        """
        return a list of file paths in all subdirectories of a path which
        have the given extension
        """
        paths_to_process = []

        for root, _, files in os.walk(path, topdown=False):
            for file_name in files:
                if file_name.endswith(extension):
                    paths_to_process.append(os.path.join(root, file_name))

        return paths_to_process
