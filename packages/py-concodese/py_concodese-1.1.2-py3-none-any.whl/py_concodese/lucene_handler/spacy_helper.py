import re

from py_concodese.lucene_handler.nlp_base import NLP, Token, TokenizedFile
# from py_concodese.translation_layer.generic_translation import GenericTranslation
from nltk.stem.porter import PorterStemmer

import en_core_web_sm
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, HYPHENS
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex, compile_suffix_regex, compile_prefix_regex
import time


class SpacyHelper(NLP):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Singleton Initializer
            cls._instance = super(SpacyHelper, cls).__new__(cls)

            cls.min_token_length = args[0] if len(args) > 0 else kwargs.get('min_token_length', 3)
            start = time.time()

            # This is the line that takes the longest to process (loading the language)
            cls.nlp = en_core_web_sm.load()

            cls.nlp.tokenizer = Tokenizer(cls.nlp.vocab)
            cls._build_prefix_patterns(cls)
            cls._build_suffix_patterns(cls)
            cls._build_infix_patterns(cls)

            cls.nltk = PorterStemmer()
            end = time.time()
            print(f"Time elapsed (Spacy singleton initializer): {end - start}")
        else:
            # Update initialization parameter 'min_token_length' if it necessary
            cls.min_token_length = args[0] if len(args) > 0 else kwargs.get('min_token_length', 3)
        return cls._instance

    def _build_prefix_patterns(self):
        prefixes = [
            r'''^[\[\("']''',
            r'''^/''',
            r'''^&lt;''',
        ]

        prefix_re = compile_prefix_regex(prefixes)
        self.nlp.tokenizer.prefix_search = prefix_re.search

    def _build_suffix_patterns(self):
        suffixes = [
            r'''[\]\)"']$''',
            r'''/$''',
            r'''&gt;$''',
        ]

        suffixes_re = compile_suffix_regex(suffixes)
        self.nlp.tokenizer.suffix_search = suffixes_re.search

    def _build_infix_patterns(self):
        infixes = (
                LIST_ELLIPSES
                + LIST_ICONS
                + [
                    r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                    r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                    ),
                    r'''[-~:$!,_(+.\'%/&;=\[]''',
                    r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                    r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                    r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
                ]
        )
        infix_re = compile_infix_regex(infixes)
        self.nlp.tokenizer.infix_finditer = infix_re.finditer

    def tokenize_list(self, texts, remove_stop_words=True) -> str:
        # """
        # tokenizes a list of strings
        # returns a single list of tokens from all strings
        # """
        return self.tokenize_string(" ".join(texts), remove_stop_words)

    def tokenize_string(self, text, remove_stop_words=True) -> list[str]:
        # """
        # Args:
        #     text - python str
        # Returns:
        #     tokens - [python str,...]
        #
        # Based on src/main/java/de/dilshener/concodese/term/extract/impl/AbstractFileTermExtractorImpl.java
        # which is called by src/main/java/de/dilshener/concodese/term/extract/impl/SourceCodeCommentExtractorImpl.java
        # """
        tokens = self.nlp(text)
        # Cleanup special characters
        result = [re.sub(r'[^A-Za-z]+', '', str(token)) for token in tokens if
                  self.filter_out_special_cases(token, remove_stop_words)]
        # Remove empty strings
        return [i for i in result if i != '']

    # def tokenize_batch(self, filename_comments_dict, remove_stop_words=True, stem_tokens=True)->list[TokenizedFile]:
    #     if self.translator is None:
    #         raise Exception("Not translator set for this tokenizer")
    #     translated_filename_comments_dict = self.translator.translate_batch_comments(filename_comments_dict)
    #
    #     tokenized_files = []
    #     for file_name, comments in translated_filename_comments_dict.items():
    #         tokenized_file = TokenizedFile(file_name)
    #
    #         tokens = self.tokenize_list(comments)
    #         [tokenized_file.add_token(token, self.stem_token(token)) for token in tokens]
    #         tokenized_files.append(tokenized_file)
    #
    #     return tokenized_files

    def filter_out_special_cases(self, token, remove_stop_words):
        # Special cases filter out:
        # numbers
        # Ids (letters followed by numbers) like Abc01234
        # File sizes like 1234k
        # Escaped special characters like &lt; &gt; &quot
        special_cases_regex = re.compile(r'^\d+$|^\S+\d+$|^\d+k|&lt;|&gt;|&quot')

        if len(token) < self.min_token_length:
            return False
        else:
            # special_characters = '!{([/*-+=~#\])}'
            token_lowcase = str(token).lower()

            if bool(special_cases_regex.search(token_lowcase)):
                return False

            if remove_stop_words:
                return token_lowcase not in self.stop_words_set

    def stem_tokens(self, tokens) -> list[str]:
        """
        Args:
            tokens - [python string, ...]
        Returns:
            stemmed_tokens - [python string, ...]
        """
        return [self.stem_token(token) for token in tokens]

    def stem_token(self, token: str) -> str:
        return self.nltk.stem(str(token))
        # stemmed_tokens = self.stem_tokens([token])
        # if len(stemmed_tokens) == 1:
        #     return stemmed_tokens[0]
        # # shouldn't have generated more than one stemmed token
        # assert len(stemmed_tokens) < 1

    def return_without_stop_words(self, tokens, mixed_case) -> list[str]:
        """returns a new list with stop words removed.
        If mixed_case: tokens are lowered before the check against stop words.
        If the tokens are already lower case, you can set mixed_case to False
        for faster execution.
        But the case of each token returned is preserved.
        """
        if mixed_case:
            return [token for token in tokens if token.lower() not in self.stop_words_set]
        return [token for token in tokens if token not in self.stop_words_set]
