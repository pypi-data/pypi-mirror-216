""" Sql model objects can be converted into these object types so that
multiprocessing can be utilised. Most of the properties of the model classes
are replicated with the exception of _id rows, and parental relationships
(e.g. a link from identifier back to the src file) as they are
not necessary. Methods are provided to both classes through the FileBase class.
"""
from __future__ import annotations
from dataclasses import dataclass

from py_concodese.storage.filebase import FileBase


def modelless_factory(model_file):
    """ creates model-less object from a model object """
    identifiers = []
    for model_identifier in model_file.identifiers:
        ident_code_tokens = [
            Token(token.text, token.stemmed_text) for token in model_identifier.tokens
        ]
        identifiers.append(
            Identifier(
                model_identifier.text, model_identifier.stemmed_text, ident_code_tokens
            )
        )

    # tokens that apply to whole file
    code_tokens = [
        Token(token.text, token.stemmed_text) for token in model_file.code_tokens
    ]
    comment_tokens = [
        Token(token.text, token.stemmed_text) for token in model_file.comment_tokens
    ]

    return File(
        id=model_file.id,
        name=model_file.name,
        stemmed_name=model_file.stemmed_name,
        package=model_file.package,
        extension=model_file.extension,
        relative_file_path=model_file.relative_file_path,
        identifiers=identifiers,
        code_tokens=code_tokens,
        comment_tokens=comment_tokens,
    )


@dataclass
class File(FileBase):
    """two files will be considered equal if their contents are the same
    BUT ORDER OF ELEMENTS MAY DIFFER"""

    id: int
    name: str
    stemmed_name: str
    package: str
    extension: str
    relative_file_path: str

    identifiers: list[Identifier]
    code_tokens: list[Token]
    comment_tokens: list[Token]

    def __hash__(self) -> int:
        # can't include the lists in the hash,
        # because the order of their elements may differ
        return hash(
            f"{self.id},"
            f"{self.name},"
            f"{self.stemmed_name},"
            f"{self.package},"
            f"{self.extension},"
            f"{self.relative_file_path},"
        )

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.stemmed_name == other.stemmed_name
            and self.package == other.package
            and self.extension == other.extension
            and self.relative_file_path == other.relative_file_path
            and set(self.identifiers) == set(other.identifiers)
            and set(self.code_tokens) == set(other.code_tokens)
            and set(self.comment_tokens) == set(other.comment_tokens)
        )


@dataclass
class Identifier:
    text: str
    stemmed_text: str
    tokens: list[Token]

    def __hash__(self) -> int:
        # can't include the lists in the hash,
        # because the order of their elements may differ
        return hash(f"{self.text},{self.stemmed_text}")

    def __str__(self) -> str:
        return f"{self.file.name.rsplit('/', 1)[1]}:{self.text}"

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.stemmed_text == other.stemmed_text
            and set(self.tokens) == set(other.tokens)
        )


# only one token class is required to keep tokens and comment tokens
@dataclass
class Token:
    text: str
    stemmed_text: str

    def __hash__(self) -> int:
        # can't include the lists in the hash,
        # because the order of their elements may differ
        return hash(f"{self.text},{self.stemmed_text}")

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.stemmed_text == other.stemmed_text
