""" A module that handles database interaction """
from __future__ import annotations

from py_concodese.storage.modelless import modelless_factory
from .sql_base import initialise
from .models import File, Identifier, Token, CommentToken
from .modelless import File as modelless_file
from sqlalchemy import select
from jpype import JClass
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SqlConnector:
    def __init__(
        self,
        file_based,
        sqlite_dir,
        clean_db=False,
        test=False,
        project_id=None,
    ) -> None:
        """_summary_

        Args:
            file_based (bool): whether to create an sqlite file or an in-memory db
            sqlite_dir (str): path to directory to contain sqlite file
            clean_db (bool, optional): Deletes any existing db. Defaults to False.
            test (bool, optional): Is this instance part of an automated test. Defaults to False.
            project_id (int, optional): An id to identify a project with. Defaults to None.
        """
        # store some sql settings in the class
        self.file_based = file_based
        self.sqlite_dir = sqlite_dir
        self.test = test
        self.project_id = project_id

        # initialise connection with sqlite
        self.session = initialise(
            file_based,
            sqlite_dir,
            clean_db,
            test,
            project_id,
        )

    def clean_db(self):
        """deletes any existing database with matching parameters to this instance"""
        # close existing connection
        self.close()

        # reinitialise session and clean db
        self.session = initialise(
            self.file_based,
            self.sqlite_dir,
            clean_db=True,
            test=self.test,
            project_id=self.project_id,
        )

    def store_tokens(self, parsed_files, tokenizer_helper, intt) -> None:
        """for each parsed file, stores identifiers, creates and stores tokens in db
        Args:
            parsed_files - list[ParsedFile]
            tokenizer_helper - instance of LuceneHelper/SpacyHelper
            intt - instance of intt
        """

        files_batch = {}

        # initialise the file row
        for idx, parsed_file in enumerate(parsed_files):
            if (idx + 1) % 50 == 0:
                logger.info(
                    f"Creating and storing tokens from files {idx + 1}/{len(parsed_files)}"
                )
                # commit changes regularly so that we don't have a massive sql
                # write, and we can keep the user updated with progress more
                # accurately
                self.session.commit()

            file_row = self.add_file_to_session(tokenizer_helper, parsed_file)

            # add each identifier
            for identifier_text in parsed_file.code_identifiers:
                identifier_row = self.add_identifier_to_session(
                    tokenizer_helper, file_row, identifier_text
                )

                # create tokens from the identifier
                tokens = intt.tokenize(identifier_text)
                self.add_tokens_to_session(
                    tokenizer_helper, tokens, identifier_row, file_row
                )
            # tokens = tokenizer_helper.tokenize_list(comment_strings)
            # stemmed_tokens = tokenizer_helper.stem_tokens(tokens)
            # for token, stemmed_token in zip(tokens, stemmed_tokens):
            #     self.session.add(CommentToken(file_row, token, stemmed_token))
            #
            # # add comments
            # self.add_comment_tokens_to_session(
            #     tokenizer_helper, file_row, parsed_file.comment_strings
            # )

            # Add file objects to a dictionary to batch tokenize below
            files_batch[parsed_file.file_name] = file_row

        self.batch_tokenize_and_translate_file_comments(files_batch, parsed_files, tokenizer_helper)

        # final write for any changes
        self.session.commit()

        logger.info(f"All tokens created")

    def batch_tokenize_and_translate_file_comments(self, files_batch, parsed_files, tokenizer_helper):
        filename_comments_dict = {parsed_file.file_name: parsed_file.comment_strings for parsed_file in parsed_files}
        tokenized_files = tokenizer_helper.tokenize_batch(filename_comments_dict, remove_stop_words=True)
        for tokenized_file in tokenized_files:
            for token in tokenized_file.tokens:
                file_object = files_batch[tokenized_file.filename]
                self.session.add(CommentToken(file_object, token.plain_token, token.stemmed_token))

    def close(self) -> None:
        """closes sessions"""
        self.session.close()

    def add_tokens_to_session(
        self,
        tokenizer_helper,
        tokens,
        identifier_row: Identifier,
        file_row: File,
    ) -> None:
        """_summary_

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            tokens (list[str]):
            identifier_row (Identifier):
            file_row (File):
        """
        stemmed_tokens = tokenizer_helper.stem_tokens(tokens)

        for token, stemmed_token in zip(tokens, stemmed_tokens):
            token_row = Token(identifier_row, token, stemmed_token, file_row)
            self.session.add(token_row)

    def add_file_to_session(self, tokenizer_helper, parsed_file) -> File:
        """adds a File object to the session

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            parsed_file (ParsedFile):

        Returns:
            File:
        """
        file_row = File(
            name=parsed_file.file_name,
            stemmed_name=tokenizer_helper.stem_token(parsed_file.file_name),
            package=parsed_file.package,
            extension=parsed_file.extension,
            relative_file_path=parsed_file.relative_file_path,
        )
        self.session.add(file_row)
        return file_row

    def add_identifier_to_session(
        self,
        tokenizer_helper,
        file_row: File,
        identifier_text: str,
    ) -> Identifier:
        """adds an Identifier object to the session

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            file_row (File):
            identifier_text (str):

        Returns:
            Identifier:
        """
        stemmed_text = tokenizer_helper.stem_token(identifier_text)
        identifier_row = Identifier(file_row, identifier_text, stemmed_text)
        self.session.add(identifier_row)
        return identifier_row

    def add_comment_tokens_to_session(
        self, tokenizer_helper, file_row: File, comment_strings
    ) -> None:
        """Adds the tokens from comment strings db session

        Args:
            tokenizer_helper (LuceneHelper/SpacyHelper):
            file_row (File):
            comment_strings (list[str]):
        """
        tokens = tokenizer_helper.tokenize_list(comment_strings)
        stemmed_tokens = tokenizer_helper.stem_tokens(tokens)
        for token, stemmed_token in zip(tokens, stemmed_tokens):
            self.session.add(CommentToken(file_row, token, stemmed_token))

    def get_src_files(
        self,
        modelless=True,
    ) -> list[modelless_file] | list[File]:
        """retrieves all src files from the db

        Args:
            modelless (bool, optional): Whether to return the db objects as a
            collection of modelless_file. Defaults to True.

        Returns:
            list[modelless_file]|list[File]:
        """
        db_src_files = self.session.query(File).all()
        if not modelless:
            return db_src_files

        logger.info("Optimising src file token data for in memory searches")
        src_files = []
        for idx, db_src_file in enumerate(db_src_files):
            if (idx + 1) % 100 == 0:
                logger.info(
                    f"Optimising src file token data for in memory searches {idx+1}/{len(db_src_files)}"
                )
            src_files.append(modelless_factory(db_src_file))
        logger.info("Optimisation complete")
        return src_files

    def get_src_file_by_name(self, name, stemmed) -> modelless_file:
        """gets the db data for a File with a matching name

        Args:
            name (_type_): name to be searched for
            stemmed (bool): whether to search the stemmed name field 

        Raises:
            Exception: if not file with that name is found

        Returns:
            modelless_file: the first matching File, converted to a modelless instance
        """
        if not stemmed:
            stmt = select(File).where(File.name == name)
        else:
            stmt = select(File).where(File.stemmed_name == name)

        for file_row in self.session.execute(stmt):
            # return first instance
            return modelless_factory(file_row._data[0])
        else:
            raise Exception("no file by that name found")

    def store_data_from_jim_derby(self, parsed_files, tokenizer_helper, db_dir):
        """extracts data from the derby database created by JIM
        and insert data into the sqlite format used by the rest of
        the application
        """

        # connect to db
        con_string = f"jdbc:derby:{db_dir};"
        sql_driver = JClass("java.sql.DriverManager").getConnection(con_string)

        # execute statement
        query_base = (
            "select file_name, identifier_name, component_word "
            "from SVM.files files join SVM.PROGRAM_ENTITIES "
            "pgm_ent on pgm_ent.file_name_key_fk = files.file_name_key "
            "join SVM.IDENTIFIER_NAMES idents on idents.identifier_name_key = "
            "pgm_ent.identifier_name_key_fk "
            "join SVM.COMPONENT_WORDS_XREFS xrefs on "
            "xrefs.identifier_name_key_fk = idents.identifier_name_key "
            "join SVM.COMPONENT_WORDS cws on cws.COMPONENT_word_key = "
            "xrefs.COMPONENT_word_key_fk "
            "WHERE SVM.files.file_name ="
        )
        query_order = "ORDER BY IDENTIFIER_NAME"

        # for each parsed src file
        for parsed_file in parsed_files:
            # add file to db session
            file_row = self.add_file_to_session(tokenizer_helper, parsed_file)

            # add comments from file
            self.add_comment_tokens_to_session(
                tokenizer_helper, file_row, parsed_file.comment_strings
            )

            # get the identifiers and tokens (comp words) for the file
            stmnt = sql_driver.createStatement()
            results = stmnt.executeQuery(
                (
                    f"{query_base} '{parsed_file.file_name}"
                    f"{parsed_file.extension}' {query_order}"
                )
            )

            comp_words = []
            identifier_row = None

            # for each result row
            while results.next():
                identifier_name = str(results.getString("identifier_name"))

                # check identifier
                if (
                    identifier_row is not None
                    and identifier_name == current_identifier_name
                    # FIXME current_identifier_name is not initialized
                ):
                    # if identifier is the same, keep collecting comp words
                    comp_words.append(str(results.getString("component_word")))
                    continue

                # when identifier changes, store comp words against old identifier
                self.add_tokens_to_session(
                    tokenizer_helper, comp_words, identifier_row, file_row
                )
                # new comp words list and identifier
                current_identifier_name = identifier_name

                identifier_row = self.add_identifier_to_session(
                    tokenizer_helper=tokenizer_helper,
                    file_row=file_row,
                    identifier_text=current_identifier_name,
                )
                comp_words = [str(results.getString("component_word"))]

            # the final identifier's tokens need to be added
            if len(comp_words) > 0:
                self.add_tokens_to_session(
                    tokenizer_helper, comp_words, identifier_row, file_row
                )
        # commit changes
        self.session.commit()
