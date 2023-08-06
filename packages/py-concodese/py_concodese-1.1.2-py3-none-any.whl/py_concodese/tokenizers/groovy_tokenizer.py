"""
This is an attempt to recreate Tezcan's groovy parser and tokeniser
as found at src/main/java/de/dilshener/concodese/term/extract/impl/SourceCodeTermExtractorImpl.java
It is deliberately non-pythonic as it is structured as close as possible to the original java
implementation.
In the original, there are a number of class level instance variables
declared under the class definition- these are declared in python as self.blah = None in the __init__
function to try to maintain similarity with the original java class structure.

The original class did not handle comments, but I have included those functions here because
only this implentation will use this kind of source code parsing. Other tokenizers will use tree
parser. The comment tokenization in this class is based on the original java implementation here:
src/main/java/de/dilshener/concodese/term/extract/impl/SourceCodeCommentExtractorImpl.java
Corresponding dictionaries for comments have been added to this class file which did not exist in
the original class. We also pass a LuceneHelper instance around that did not exist in the java
implementation.

Cannot use pylucene because it also requires the starting of a separate jvm and causes an error.
"""
from jpype import JClass
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


# in concodese original, this class is called TermExtractorImpl
class GroovyTokenizer:

    groovy_keywords = [
        "abstract",
        "as",
        "assert",
        "boolean",
        "break",
        "byte",
        "case",
        "catch",
        "char",
        "class",
        "const",
        "continue",
        "def",
        "default",
        "do",
        "double",
        "else",
        "enum",
        "extends",
        "false",
        "final",
        "finally",
        "float",
        "for",
        "goto",
        "if",
        "implements",
        "import",
        "in",
        "instanceof",
        "int",
        "interface",
        "long",
        "native",
        "new",
        "null",
        "package",
        "private",
        "protected",
        "public",
        "return",
        "short",
        "static",
        "strictfp",
        "super",
        "switch",
        "synchronized",
        "this",
        "threadsafe",
        "throw",
        "throws",
        "transient",
        "true",
        "try",
        "void",
        "volatile",
        "while",
        "string",
        "comparable",
        "map",
        "hashmap",
        "list",
        "set",
        "get",
        "integer",
        "object",
    ]

    def __init__(self, extension=".groovy"):
        """ Tokenizes .groovy extension by default """
        self.extension = extension

        # intt identifier tokenisation
        self.factory = None
        self.ident_tokeniser = None

        # dictionary of extracted term --> no of occurrences
        # INDENTIFIER NAMES---<COMPONENT_WORDS_XREF>---COMPONENT_WORDS
        self.identifier_terms_map = None

        # dictionary of class-->identifiers-->terms
        # FILES---<PROGRAM_ENTITIES>---INDENTIFIER NAMES
        self.file_identifiers_map = None

        # dictionary of package-->files-->identifiers-->terms
        self.package_files_map = None

        # dictionary of file-->comments
        self.file_comments_map = None

        # ignores the groovy keywords
        self.groovy_stop_analyzer = None

        # breaks up the line into individual words
        self.white_space_analyzer = None

        self.package_name = None
        self.space_stream = None
        self.groovy_stream = None

        # an enum that's handy to store so we don't have to convert from java so often
        self.version_lucene_36 = JClass("org.apache.lucene.util.Version").LUCENE_36

    def perform_extraction(self, project_path):
        """ returns a tuple of dictionaries (package_files_map, file_comments_map)"""
        # intt instantiation
        self.initialize()

        self.list_files_for_folder(project_path)

        return self.package_files_map, self.file_comments_map

    def initialize(self):
        ident_factory_class = JClass(
            "uk.ac.open.crc.intt.IdentifierNameTokeniserFactory"
        )
        self.factory = ident_factory_class()
        self.ident_tokeniser = self.factory.create()

        # analyzer instantiation
        self.groovy_stop_analyzer = JClass("org.apache.lucene.analysis.StopAnalyzer")(
            self.version_lucene_36,
            JClass("java.util.HashSet")(GroovyTokenizer.groovy_keywords),
        )

        self.white_space_analyzer = JClass(
            "org.apache.lucene.analysis.WhitespaceAnalyzer"
        )(self.version_lucene_36)

        # prepare/ empty the in memory dictionaries
        self.identifier_terms_map = {}  # string -> [string]
        self.file_identifiers_map = {}  # string -> {string -> [string]}
        self.package_files_map = {}  # string -> {string -> {string -> [string]}}

        self.file_comments_map = {}  # string -> [string]

    def list_files_for_folder(self, path):
        """
        Iterate thru the entries found in the specified directory and process those
        ones that ends with .groovy and .java
        """

        for root, _, files in os.walk(path, topdown=False):
            for file_name in files:
                if file_name.endswith(self.extension):
                    self.process_file_content(os.path.join(root, file_name))

    def process_file_content(self, file_path):
        """
        This method reads in an input text file such as a source code file and iterates
        over the input lines to extract terms.
        """
        logging.debug(f"Processing {file_path}")

        self.file_identifiers_map = {}  # string -> {string -> [string]}
        self.identifier_terms_map = {}  # string -> [string]

        # read and tokenize the input file
        with open(file_path) as f:
            # unlikely to cause a memory error in the size of files we're working with
            lines = f.read().splitlines()
            # note that by this point files have already been checked for a valid .groovy suffix
            file_name = Path(file_path).stem

            # initialise file comments dictionary
            self.file_comments_map[file_name] = []

        for line in lines:
            input_line = line.strip()
            # only process lines that are package/class/methods signatures
            if input_line.startswith(
                (
                    "package",
                    "public",
                    "private",
                    "class",
                    "protected",
                    "abstract",
                    "static",
                    "import",
                )
            ):
                self.do_split(input_line, file_name)
            elif input_line.startswith(
                (
                    "/*",
                    "*",
                    "*/",
                    "//",
                )
            ):
                self.store_comment_line(input_line, file_name)

            # check every line for in line comments regardless
            # if (
            #     "/*",
            #     "*",
            #     "*/",
            #     "//",
            # ) in input_line:
            #     self.store_in_line_comments(input_line, file_name)

        # if no identifiers can be extracted from the class body,
        # then use the class name as identifier to split it into terms and put them in identiferTermsMap for later save
        if len(self.identifier_terms_map) == 0:
            self.identifier_terms_map[f"{file_name};3"] = [
                list(self.ident_tokeniser.tokenise(file_name))
            ]

        # FILES---<PROGRAM_ENTITIES>---INDENTIFIER NAMES
        # 1. every time a file is processed with its identifiers/terms add it into the file/identifiers map
        if file_name not in self.file_identifiers_map:
            self.file_identifiers_map[file_name] = {}
        self.file_identifiers_map[file_name] = self.identifier_terms_map.copy()

        # 2. add the file/identifiers into the package map
        if self.package_name not in self.package_files_map:
            self.package_files_map[self.package_name] = {}
        self.package_files_map[self.package_name] = {
            **self.package_files_map[self.package_name],
            **self.file_identifiers_map,
        }

        self.identifier_terms_map = None
        self.file_identifiers_map = None

        if self.groovy_stream is not None:
            self.groovy_stream.end()
            self.groovy_stream.close()

        if self.space_stream is not None:
            self.space_stream.end()
            self.space_stream.close()

    def do_split(self, text, file_name):
        """
        This method obtains a token stream from the WhiteSpaceAnalyzer and iterates over the CharTermAttribute to extract
        the terms. It than uses the StopWordAnalyzer to determine if the extracted term is a groovy keywords and if it is
        not it calls INTT tokenizer to split the extracted terms into individual hard_words using camelcase etc.
        """

        # use space tokenizer to split
        self.space_stream = self.white_space_analyzer.tokenStream(
            "contents", JClass("java.io.StringReader")(text)
        )

        # get the term attribute from the token stream
        char_term_attr_class = JClass(
            "org.apache.lucene.analysis.tokenattributes.CharTermAttribute"
        )
        term_attr = self.space_stream.addAttribute(char_term_attr_class)

        while self.space_stream.incrementToken():
            identifier = term_attr.toString()
            identifier = str(identifier)  # try making it a python string

            if identifier == "package":
                self.space_stream.incrementToken()
                identifier = term_attr.toString()
                self.package_name = identifier.replace(
                    ";", ""
                )  # may be present as a line terminator
                break  # no need to process package name further, it is used later as ref

            # handle method signature
            identifier = identifier.strip("{").strip(")")  # order may be important

            candidate_identifier = identifier.split("(")
            for i, identifier in enumerate(candidate_identifier):
                # use stop word analyzer to elimate groovy language keywords
                self.groovy_stream = self.groovy_stop_analyzer.tokenStream(
                    "contents", JClass("java.io.StringReader")(identifier)
                )

                # get the term attr from the token stream
                term_attr_groovy = self.groovy_stream.addAttribute(char_term_attr_class)

                # for each identifier, split it into terms using INTT based on patterns
                while self.groovy_stream.incrementToken():
                    ident_for_split = term_attr_groovy.toString()
                    hard_words = self.ident_tokeniser.tokenise(ident_for_split)

                    # may be present as a line terminator,
                    # the empty space should be discarded in the end if it's not needed, but it'll
                    # also act as a seperator from inline comments following a semi-colon without
                    # a space.
                    identifier = identifier.replace(";", "")

                    # INDENTIFIER NAMES---<COMPONENT_WORDS_XREF>---COMPONENT_WORDS
                    # 7 = FIELD, species key used later as xref
                    identifier_key = f"{identifier};7"  # 7 = everything else?
                    # if candidate identifier is a method name
                    # i.e. the left hand side of the bracket, then it is a method=14
                    if len(candidate_identifier) > 1 and i == 0:
                        identifier_key = f"{identifier};15"  # 15 = method, species key used later as xref
                    if file_name == identifier:
                        identifier_key = (
                            f"{identifier};3"  # 3 = class, species key for FILES
                        )
                    if "class" in text and file_name != identifier:
                        identifier_key = f"{identifier};14"  # 14 = member class, species key for FILES

                    if identifier_key not in self.identifier_terms_map:
                        self.identifier_terms_map[identifier_key] = []
                    self.identifier_terms_map[identifier_key] += list(hard_words)

    def store_comment_line(self, input_line, file_name):
        """ tokenizes the comment line into words and stores them """
        self.file_comments_map[file_name].append(input_line)

    def store_in_line_comments(self, input_line, file_name):
        """ todo """
        pass
