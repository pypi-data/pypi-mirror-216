from __future__ import annotations
from jpype import JClass, java
import logging

logger = logging.getLogger(__name__)


class Intt:
    """ A wrapper around the INTT jar """

    def __init__(self) -> None:
        ident_factory_class = JClass(
            "uk.ac.open.crc.intt.IdentifierNameTokeniserFactory"
        )
        self.factory = ident_factory_class()
        self.factory.setRecursiveSplitOn()  # option set in java-concodese
        self.factory.seModalExpansionOn()  # option set in java-concodese
        self.ident_tokeniser = self.factory.create()

        self._backup_tokenizers = []

    @property
    def backup_tokenizers(self) -> list:
        """lazily creates INTT tokenizers with different flags.
        If an error is raised by a tokenizer, these other tokenizers can try
        to tokenize an identifier.

        Returns:
            list: of INTT tokenizers
        """
        if len(self._backup_tokenizers) != 0:
            return self._backup_tokenizers

        # create tokenizers with different flag options each tokenizer
        #  will be maintaining its own internal dictionary of tokens
        flag_variations = [
            (True, False),
            (False, True),
            (False, False),
        ]
        for variation in flag_variations:
            self.factory.setRecursiveSplitOff()
            self.factory.seModalExpansionOff()
            if variation[0]:
                self.factory.setRecursiveSplitOn()
            if variation[1]:
                self.factory.seModalExpansionOn()

            self._backup_tokenizers.append(self.factory.create())

        return self.backup_tokenizers

    def tokenize(self, identifier) -> list[str]:
        """Uses INTT to split an identifier into (lower case) tokens

        Args:
            identifier (str):

        Returns:
            list[str]: tokens
        """

        # split the identifier if it contains '.'
        identifier_parts = identifier.split(".")
        tokens = []  # stores tokens

        # start with the preferred tokenizer
        tokenizers = [self.ident_tokeniser]

        for part in identifier_parts:
            n = 0
            # try to tokenize with every available tokenizer until one works
            while n < len(tokenizers):
                try:
                    tokens += [
                        (str(token)).lower()
                        for token in self.ident_tokeniser.tokenise(part)
                    ]
                    break  # no exception, so break the while loop here
                except java.lang.StringIndexOutOfBoundsException:
                    # get backup tokenizers if they haven't already been added
                    if len(tokenizers) == 1:
                        tokenizers += self.backup_tokenizers
                    logger.warning(
                        f"Exception trying to tokenize: '{part}', will retry"
                    )
                    if n == len(tokenizers) - 1:
                        logger.warning(
                            f"Final attempt to tokenize failed: '{part}'",
                        )
                n += 1

        return tokens
