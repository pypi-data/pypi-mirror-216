""" a set of classes that provide base functionality that is shared between
model and modelless objects
"""
from __future__ import annotations
from enum import Enum


class TermTypes(Enum):
    identifier = 0
    code_token = 1
    comment_token = 2
    code_and_comments = 3


class FileBase:
    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @property
    def namespace_path(self) -> str:
        """ returns class path including extension """
        return f"{self.package}.{self.name}{self.extension}"

    @property
    def name_with_ext(self) -> str:
        """ returns file name including extension """
        return f"{self.name}{self.extension}"

    @staticmethod
    def pre_cache_terms(src_file) -> FileBase:
        """ caches term lists and sets before they're required """
        for term_type in TermTypes:
            for stemmed in [False, True]:
                # lists are also cached in the creation of the set
                src_file.get_term_set(term_type, stemmed)
        return src_file

    def get_term_set(self, term_type, stemmed) -> set(str):
        """returns a set of terms for this file

        Args:
            term_type (TermTypes): the type of terms to be returned
            stemmed(bool): whether the terms should be stemmed

        Returns:
            set(str):
        """
        # check if term set has already been created
        if hasattr(self, "term_sets"):
            term_set = self.term_sets.get((term_type, stemmed), None)
            if term_set is not None:
                return term_set
        else:
            self.term_sets = {}  # (TermTypes, bool) -> set()

        term_set = self._create_terms_set(term_type, stemmed)
        self.term_sets[(term_type, stemmed)] = term_set
        return term_set

    def get_term_list(self, term_type, stemmed) -> list[str]:
        """returns a list of terms for this file

        Args:
            term_type (TermTypes): the type of terms to be returned
            stemmed(bool): whether the terms should be stemmed

        Returns:
            list[str]:
        """

        # check if term list is cached before creating """
        if hasattr(self, "term_lists"):
            term_list = self.term_lists.get((term_type, stemmed), None)
            if term_list is not None:
                return term_list
        else:
            self.term_lists = {}  # (TermTypes, bool) -> []

        term_list = self._create_terms_list(term_type, stemmed)
        self.term_lists[(term_type, stemmed)] = term_list
        return term_list

    def _create_terms_list(self, term_type, stemmed) -> list[str]:
        """creates a list of terms present in a file

        Args:
            term_type (TermTypes): the type of terms to be returned
            stemmed (bool): whether the terms should be stemmed

        Returns:
            list[str]:
        """
        if term_type is TermTypes.identifier:
            collection = self.identifiers
        elif term_type is TermTypes.code_token:
            collection = self.code_tokens
        elif term_type is TermTypes.comment_token:
            collection = self.comment_tokens
        elif term_type is TermTypes.code_and_comments:
            terms = self.get_term_list(
                TermTypes.code_token, stemmed
            ) + self.get_term_list(TermTypes.comment_token, stemmed)
            return terms

        if not stemmed:
            terms = [(word.text).lower() for word in collection]
        else:  # stemmed
            terms = [(word.stemmed_text.lower()) for word in collection]

        return terms

    def _create_terms_set(self, term_type, stemmed) -> set[str]:
        """creates a term set from term list

        Args:
            term_type (TermTypes): the type of terms to be returned
            stemmed (bool): whether the terms should be stemmed

        Returns:
            set[str]:
        """
        return set(self.get_term_list(term_type, stemmed))
