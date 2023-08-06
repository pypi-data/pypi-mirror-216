from __future__ import annotations
from jpype import JClass
from py_concodese.lucene_handler.nlp_base import NLP


class LuceneHelper(NLP):
    """ A class to handle interacts with lucene in the JVM """

    def __init__(self, min_token_length=3) -> None:
        super().__init__(min_token_length)
        self.version_lucene_36 = JClass("org.apache.lucene.util.Version").LUCENE_36
        self.char_term_attr_class = JClass(
            "org.apache.lucene.analysis.tokenattributes.CharTermAttribute"
        )
        self.stop_words_hash_set = JClass("java.util.HashSet")(self.stop_words_list)
        self.min_token_length = min_token_length

    def tokenize_list(self, texts, remove_stop_words=True) -> list[str]:
        """tokenizes a list of strings

        Args:
            texts (list[str]): texts to be tokenized
            remove_stop_words (bool, optional): remove stop words prior to tokenization.
            Defaults to True.

        Returns:
            list[str]: all tokens from all texts
        """
        return self.tokenize_string(" ".join(texts), remove_stop_words)

    def tokenize_string(self, text, remove_stop_words=True) -> list[str]:
        """tokenizes a string

        Args:
            text - (python) str
        Returns:
            tokens - [python str,...]

        Based on src/main/java/de/dilshener/concodese/term/extract/impl/AbstractFileTermExtractorImpl.java
        which is called by src/main/java/de/dilshener/concodese/term/extract/impl/SourceCodeCommentExtractorImpl.java
        """
        tokens = []
        if text is None:
            return tokens

        # if self.translator:
        #     text = self.translator.translate(text, language_code='EN')

        if remove_stop_words:
            white_space_analyzer = JClass("org.apache.lucene.analysis.StopAnalyzer")(
                self.version_lucene_36, self.stop_words_hash_set
            )

        else:
            white_space_analyzer = JClass(
                "org.apache.lucene.analysis.standard.StandardAnalyzer"
            )(self.version_lucene_36)

        space_stream = white_space_analyzer.tokenStream(
            "contents", JClass("java.io.StringReader")(text)
        )

        term_attr = space_stream.addAttribute(self.char_term_attr_class)

        while space_stream.incrementToken():
            word = str(term_attr.toString())
            if len(word.strip()) >= self.min_token_length:
                tokens.append(word)

        space_stream.close()

        return tokens

    def stem_tokens(self, tokens) -> list[str]:
        """stems tokens

        Args:
            tokens - [python string, ...]
        Returns:
            stemmed_tokens - [python string, ...]
        """
        stemmed_tokens = []

        # combine tokens into single string
        combined_tokens = " ".join([str(token) for token in tokens])

        if len(combined_tokens) == 0:
            return stemmed_tokens

        white_space_analyzer = JClass("org.apache.lucene.analysis.WhitespaceAnalyzer")(
            self.version_lucene_36
        )

        space_stream = white_space_analyzer.tokenStream(
            "contents", JClass("java.io.StringReader")(combined_tokens)
        )

        stemmer = JClass("org.apache.lucene.analysis.PorterStemFilter")(space_stream)

        stemmer.reset()

        token = stemmer.addAttribute(self.char_term_attr_class)

        while stemmer.incrementToken():
            stemmed_tokens.append(str(token.toString()))

        space_stream.close()
        stemmer.close()

        return stemmed_tokens

    def stem_token(self, token: str) -> str:
        """_summary_

        Args:
            token (str): token to stem

        Returns:
            str: tokenized string
        """
        stemmed_tokens = self.stem_tokens([token])
        if len(stemmed_tokens) == 1:
            return stemmed_tokens[0]
        # shouldn't have generated more than one stemmed token
        assert len(stemmed_tokens) < 1

    def return_without_stop_words(self, tokens, mixed_case) -> list[str]:
        """returns a new list with stop words removed. Case is always preserved.

        Args:
            tokens (list[str]):
            mixed_case (bool): if true, a lower case version of each token is
            compared against the stop list. This results is slower execution.

        Returns:
            list[str]:
        """

        if mixed_case:
            return [token for token in tokens if token.lower() not in self.stop_words_set]
        return [token for token in tokens if token not in self.stop_words_set]

#
# stop_words_list = [
#     "a",
#     "about",
#     "above",
#     "above",
#     "across",
#     "after",
#     "afterwards",
#     "again",
#     "against",
#     "all",
#     "almost",
#     "alone",
#     "along",
#     "already",
#     "also",
#     "although",
#     "always",
#     "am",
#     "among",
#     "amongst",
#     "amoungst",
#     "amount",
#     "an",
#     "and",
#     "another",
#     "any",
#     "anyhow",
#     "anyone",
#     "anything",
#     "anyway",
#     "anywhere",
#     "are",
#     "around",
#     "as",
#     "at",
#     "back",
#     "be",
#     "became",
#     "because",
#     "become",
#     "becomes",
#     "becoming",
#     "been",
#     "before",
#     "beforehand",
#     "behind",
#     "being",
#     "below",
#     "beside",
#     "besides",
#     "between",
#     "beyond",
#     "bill",
#     "both",
#     "bottom",
#     "but",
#     "by",
#     "call",
#     "can",
#     "cannot",
#     "cant",
#     "co",
#     "con",
#     "could",
#     "couldnt",
#     "cry",
#     "de",
#     "describe",
#     "detail",
#     "do",
#     "done",
#     "down",
#     "due",
#     "during",
#     "each",
#     "eg",
#     "eight",
#     "either",
#     "eleven",
#     "else",
#     "elsewhere",
#     "empty",
#     "enough",
#     "etc",
#     "even",
#     "ever",
#     "every",
#     "everyone",
#     "everything",
#     "everywhere",
#     "except",
#     "few",
#     "fifteen",
#     "fify",
#     "fill",
#     "find",
#     "fire",
#     "first",
#     "five",
#     "for",
#     "former",
#     "formerly",
#     "forty",
#     "found",
#     "four",
#     "from",
#     "front",
#     "full",
#     "further",
#     "get",
#     "give",
#     "go",
#     "had",
#     "has",
#     "hasnt",
#     "have",
#     "he",
#     "hence",
#     "her",
#     "here",
#     "hereafter",
#     "hereby",
#     "herein",
#     "hereupon",
#     "hers",
#     "herself",
#     "him",
#     "himself",
#     "his",
#     "how",
#     "however",
#     "hundred",
#     "ie",
#     "if",
#     "in",
#     "inc",
#     "indeed",
#     "interest",
#     "into",
#     "is",
#     "it",
#     "its",
#     "itself",
#     "keep",
#     "last",
#     "latter",
#     "latterly",
#     "least",
#     "less",
#     "ltd",
#     "made",
#     "many",
#     "may",
#     "me",
#     "meanwhile",
#     "might",
#     "mill",
#     "mine",
#     "more",
#     "moreover",
#     "most",
#     "mostly",
#     "move",
#     "much",
#     "must",
#     "my",
#     "myself",
#     "name",
#     "namely",
#     "neither",
#     "never",
#     "nevertheless",
#     "next",
#     "nine",
#     "no",
#     "nobody",
#     "none",
#     "noone",
#     "nor",
#     "not",
#     "nothing",
#     "now",
#     "nowhere",
#     "of",
#     "off",
#     "often",
#     "on",
#     "once",
#     "one",
#     "only",
#     "onto",
#     "or",
#     "other",
#     "others",
#     "otherwise",
#     "our",
#     "ours",
#     "ourselves",
#     "out",
#     "over",
#     "own",
#     "part",
#     "per",
#     "perhaps",
#     "please",
#     "put",
#     "rather",
#     "re",
#     "same",
#     "see",
#     "seem",
#     "seemed",
#     "seeming",
#     "seems",
#     "serious",
#     "several",
#     "she",
#     "should",
#     "show",
#     "side",
#     "since",
#     "sincere",
#     "six",
#     "sixty",
#     "so",
#     "some",
#     "somehow",
#     "someone",
#     "something",
#     "sometime",
#     "sometimes",
#     "somewhere",
#     "still",
#     "such",
#     "system",
#     "take",
#     "ten",
#     "than",
#     "that",
#     "the",
#     "their",
#     "them",
#     "themselves",
#     "then",
#     "thence",
#     "there",
#     "thereafter",
#     "thereby",
#     "therefore",
#     "therein",
#     "thereupon",
#     "these",
#     "they",
#     "thickv",
#     "thin",
#     "third",
#     "this",
#     "those",
#     "though",
#     "three",
#     "through",
#     "throughout",
#     "thru",
#     "thus",
#     "to",
#     "together",
#     "too",
#     "top",
#     "toward",
#     "towards",
#     "twelve",
#     "twenty",
#     "two",
#     "un",
#     "under",
#     "until",
#     "up",
#     "upon",
#     "us",
#     "very",
#     "via",
#     "was",
#     "we",
#     "well",
#     "were",
#     "what",
#     "whatever",
#     "when",
#     "whence",
#     "whenever",
#     "where",
#     "whereafter",
#     "whereas",
#     "whereby",
#     "wherein",
#     "whereupon",
#     "wherever",
#     "whether",
#     "which",
#     "while",
#     "whither",
#     "who",
#     "whoever",
#     "whole",
#     "whom",
#     "whose",
#     "why",
#     "will",
#     "with",
#     "within",
#     "without",
#     "would",
#     "yet",
#     "you",
#     "your",
#     "yours",
#     "yourself",
#     "yourselves",
#     "the",
# ]
#
# stop_words_set = set(stop_words_list)
