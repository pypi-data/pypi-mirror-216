from __future__ import annotations
from enum import Enum
import importlib
from py_concodese.tokenizers.groovy_tokenizer import GroovyTokenizer
from py_concodese.tokenizers.java_parser import JavaParser
from py_concodese.tokenizers.php_parser import PhpParser
from py_concodese.tokenizers.c_sharp_parser import CSHARPParser
from py_concodese.tokenizers.rust_parser import RustParser
from py_concodese.tokenizers.tree_sitter_base import TreeSitterParser
from py_concodese.tokenizers.java_parser_supplementary import JavaParserSupplementary


class ProgrammingLanguage:
    _id: int
    name: str
    parser: str

    def __init__(self, _id: int, name: str, parser: str, module_path:str):
        self._id = _id
        self.name = name
        self.parser = parser
        self.module_path = module_path

    def __eq__(self, other):
        return self._id == other

    def __hash__(self):
        # This is necessary, so it can be put in the available_languages set in the ParserFactory
        return self._id

    def __str__(self):
        return f"ProgrammingLanguage {self._id} - {self.name}"

    def __repr__(self):
        return self.__str__()


class ParserFactory:
    def __init__(self, grammar_path):
        self.grammar_path = grammar_path
        # if you want to toggle on/ off language functionality,
        # this is the place to do it.
        self.available_languages = {
            # Old parser
            ProgrammingLanguage(0, 'groovy', 'GroovyTokenizer', 'py_concodese.tokenizers.groovy_tokenizer'),
            ProgrammingLanguage(1, 'java', 'JavaParser', 'py_concodese.tokenizers.java_parser'),
            ProgrammingLanguage(6, 'php', 'PhpParser', 'py_concodese.tokenizers.php_parser'),
            ProgrammingLanguage(7, 'c#', 'CSHARPParser', 'py_concodese.tokenizers.c_sharp_parser'),
            ProgrammingLanguage(8, 'rust', 'RustParser', 'py_concodese.tokenizers.rust_parser')

            # As for the Jim parser, it is requested via get_java_supplementary_parser(self):

        }

    def __contains__(self, language_id):
        return language_id in [language._id for language in self.available_languages]

    def __getitem__(self, language_id):
        for language in self.available_languages:
            if language._id == language_id:
                return language
        raise KeyError(f'Language with id {language_id} is not defined')

    def get_item_from_language_name(self, language_name):
        for language in self.available_languages:
            if language.name == language_name:
                return language
        raise KeyError(f'Language with name {language_name} is not defined')

    def add_language(self, language: ProgrammingLanguage):
        # if language in self:
        #     raise KeyError('Language id already defined')
        if language in self.available_languages:
            raise KeyError('Language id already defined')
        self.available_languages.add(language)

    def get_available_languages_id(self):
        return [language._id for language in self.available_languages]

    def get_available_languages_names(self):
        return set([language.name for language in self.available_languages])

    def get_java_supplementary_parser(self):
        java_sup = ProgrammingLanguage(5, 'java', 'JavaParserSupplementary', 'py_concodese.tokenizers.java_parser_supplementary')
        return self._create_instance_from_language_class_name(java_sup)

    def create_parser(self, programming_language_id) -> GroovyTokenizer | TreeSitterParser:
        """Creates a parser

        Args:
            programming_language_id (ProgrammingLanguage): the language the parser
            will parse

        Raises:
            ValueError: if programming_language does not have a parser

        Returns:
            GroovyTokenizer | TreeSitterParser
        """
        if programming_language_id not in self.available_languages:
            raise ValueError("Programming language does not have a parser")

        # This searches in the available_languages set for the language with
        # the given id, thanks to the __getitem__ method
        programming_language = self[programming_language_id]

        return self._create_instance_from_language_class_name(programming_language)

    def create_parsers_from_language_names(self, language_names:[str])-> [GroovyTokenizer | TreeSitterParser]:
        parsers = []
        for language in language_names:
            programming_language = self.get_item_from_language_name(language)
            parsers.append(self._create_instance_from_language_class_name(programming_language))
        return parsers
        # raise ValueError("Programming language does not have a parser")

    def _create_instance_from_language_class_name(self, programming_language):
        module = importlib.import_module(programming_language.module_path)
        class_ = getattr(module, programming_language.parser)
        return class_(self.grammar_path)

        # Alternative way to do it (using globals())
        # Unfortunately this fails in some tests
        # language_class = globals()[programming_language.parser]
        # return language_class(self.grammar_path)

#
# class ProgrammingLanguage(Enum):
#     GROOVY = 0
#     JAVA = 1
#     PYTHON = 2
#     # C = 3
#     # CPP = 4
#     JAVA_SUPPLEMENTARY = 5
#     PHP = 6
#     CSHARP = 7
#     RUST = 8
#
#
# # if you want to toggle on/ off language functionality,
# # this is the place to do it.
# language_string_to_enum = {
#     "groovy": ProgrammingLanguage.GROOVY,
#     "java": ProgrammingLanguage.JAVA,
#     "python": ProgrammingLanguage.PYTHON,
#     # "c": ProgrammingLanguage.C,
#     # "c++": ProgrammingLanguage.CPP,
#     "php": ProgrammingLanguage.PHP,
#     "c#": ProgrammingLanguage.CSHARP,
#     "rust": ProgrammingLanguage.RUST,
# }
#
#
# def create_parser(
#     programming_language, grammar_path
# ) -> GroovyTokenizer | TreeSitterParser:
#     """Creates a parser
#
#     Args:
#         programming_language (ProgrammingLanguage): the language the parser
#         will parse
#         grammar_path (str): path to grammar directory
#
#     Raises:
#         ValueError: if programming_language does not have a parser
#
#     Returns:
#         GroovyTokenizer | TreeSitterParser
#     """
#     if programming_language is ProgrammingLanguage.GROOVY:
#         # old
#         return GroovyTokenizer()
#
#     if programming_language is ProgrammingLanguage.JAVA:
#         return JavaParser(grammar_path)
#     # if programming_language is ProgrammingLanguage.C:
#     #     return CParser(grammar_path)
#     # if programming_language is ProgrammingLanguage.CPP:
#     #     return CPPParser(grammar_path)
#     if programming_language is ProgrammingLanguage.JAVA_SUPPLEMENTARY:
#         return JavaParserSupplementary(grammar_path)
#     if programming_language is ProgrammingLanguage.PHP:
#         return PhpParser(grammar_path)
#     if programming_language is ProgrammingLanguage.CSHARP:
#         return CSHARPParser(grammar_path)
#     if programming_language is ProgrammingLanguage.RUST:
#         return RustParser(grammar_path)
#
#     raise ValueError("Programming language does not have a parser")


