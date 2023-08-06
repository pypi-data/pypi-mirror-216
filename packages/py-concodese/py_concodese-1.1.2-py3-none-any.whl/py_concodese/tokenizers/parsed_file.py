""" The datastructure that a file can be converted into before tokenization """
from __future__ import annotations


class ParsedFile:
    def __init__(self, file_name, extension, relative_file_path) -> None:
        """_summary_

        Args:
            file_name (str):
            extension (str): should include preceding stop (.)
            relative_file_path (str): path relative to the root directory of the project
        """
        self.package = None
        self.file_name = file_name
        self.extension = extension
        self.code_identifiers = []
        self.comment_strings = []
        self.relative_file_path = relative_file_path

    def set_package(self, package, overwrite=False) -> None:
        """sets the package of the instance, can only be set once,
        unless overwrite is True

        Args:
            package (str):
            overwrite (bool, optional): Allows the package to be overwritten.
            Defaults to False.
        """
        if self.package is None or overwrite:
            self.package = package

    def add_code_identifier(self, ident) -> None:
        """Adds a code identifier to the list

        Args:
            ident (str):
        """
        self.code_identifiers.append(ident)

    def add_comment_string(self, comment) -> None:
        """Adds a comment string to the list of comments

        Args:
            comment (str):
        """
        self.comment_strings.append(comment)

    @staticmethod
    def find_parsed_file_by_name(parsed_files, name) -> ParsedFile:
        """ returns the first parsed file with a matching name """
        for parsed_file in parsed_files:
            if parsed_file.file_name == name:
                return parsed_file
        return None
