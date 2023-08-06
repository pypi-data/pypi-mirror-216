from py_concodese.lucene_handler.lucene_helper import LuceneHelper
from py_concodese.lucene_handler.spacy_helper import SpacyHelper
from py_concodese.lucene_handler.nlp_base import NLP
from py_concodese.scoring.vsm import VSM
from py_concodese.tokenizers.intt import Intt
from py_concodese.tokenizers.parser_factory import ParserFactory
import shutil
from jpype import JClass
from os.path import join
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Indexer:

    def __init__(self, parser_factory: ParserFactory, sql_connector):
        """
            Args:
                grammar_path (str): path to grammar directory
                sql_connector (SqlConnector):
        """
        self.parser_factory = parser_factory
        self.sql_connector = sql_connector
        # self.tokenizer = tokenizer

    def parse_and_store_src_tokens(self, src_path, src_languages, tokenizer:NLP) -> int:
        """parses src files and stores data and tokens in sqlite

        Args:
            src_path (str): path to source files
            src_languages (list[str]): list of source languages

        Returns:
            int: number of files parsed
        """
        parsers = self.parser_factory.create_parsers_from_language_names(src_languages)

        parsed_files = []
        for idx, parser in enumerate(parsers):
            logger.info(f"Beginning to parse {src_languages[idx]} source code")
            parsed_files += parser.perform_extraction(src_path)

        logger.info(f"Parsing complete. Storing tokens in database (ignore SLF4J warnings)")
        self.sql_connector.store_tokens(parsed_files, tokenizer, Intt())

        return len(parsed_files)

    def _get_all_available_parsers(self):
        return [self.parser_factory.create_parser(language.id) for language in self.parser_factory.available_languages]

    def parse_and_store_src_tokens_with_jim(self, src_path, derby_path,
                                            delete_derby_db_after, tokenizer:NLP, project_id=None, ) -> int:
        """_summary_

        Args:
            src_path (str): path to source files
            derby_path (str): directory to store derby data in
            delete_derby_db_after (bool): whether to delete the derby data after parsing
            project_id (int, optional): . Defaults to None.

        Returns:
            int: number of files parsed
        """

        # there can be multiple reindex requests so derby needs a unique folder
        derby_id = project_id if project_id is not None else -1
        derby_path = join(derby_path, str(derby_id))

        # delete the old derby database if it exists
        Indexer.delete_derby_database(derby_path)

        # jim to tokenize src code
        jim = JClass("uk.ac.open.crc.jim.Jim")

        main_args = [
            "-p=" + src_path,
            "-v=" + str(derby_id),
            # "-d=" + "/home/danny/Documents/repos/concodese-java/projects/databases/derby/SWTv3.1"
            "-d=" + derby_path,
            "-t",  # include test code
            "-intt-recursive",  # splitter more aggressive
            "-intt-modal-expansion",  # expands negated modal verbs e.g. "cant" to "can not"
            src_path,
        ]

        logger.info(f"JIM is starting to parse java source code")

        jim.main(main_args)

        # use our regular parser to get some supplementary data
        java_parser = self.parser_factory.get_java_supplementary_parser()
        parsed_files = java_parser.perform_extraction(src_path)

        # extract data from derby database
        self.sql_connector.store_data_from_jim_derby(
            parsed_files,
            tokenizer,
            derby_path,
        )

        # delete the derby database when finished
        if delete_derby_db_after:
            logger.info(f"Deleting derby database in {derby_path}")
            Indexer.delete_derby_database(derby_path)

        return len(parsed_files)

    @staticmethod
    def delete_derby_database(db_dir):
        """deletes the derby database folder

        Args:
            db_dir ():
        """
        try:
            shutil.rmtree(db_dir, ignore_errors=False, onerror=None)
        except FileNotFoundError as e1:
            logger.warning(f"Derby database already deleted: {e1.filename}")
        except Exception as e:
            pass  # it's just easier to ask for forgiveness than permission
            logger.warning(f"Exception when deleting derby database: {e}")


    def reindex_src(self,
            src_path,
            src_languages,
            # grammar_path,
            VSM_path,
            # sql_connector,
            tokenizer:NLP,
            project_id=None,
    ) -> list:
        """creates and stores all data needed from source files: tokens and vsm indexes
        Args:
            src_path (str): path to source files
            src_languages (list[str]): list of source languages
            grammar_path (str): path to grammar directory
            VSM_path (str): path to store vsm data
            sql_connector (SqlConnector):

        Returns:
            list: collection of source file objects parsed
        """
        # clean database before indexing
        self.sql_connector.clean_db()

        num_of_parsed_files = self.parse_and_store_src_tokens(
            src_path,
            src_languages,
            # grammar_path,
            # sql_connector,
            tokenizer=tokenizer
        )

        src_files = self.sql_connector.get_src_files()

        create_vsm_indexes(VSM_path, src_files, project_id)

        return src_files


    def reindex_src_with_jim(self,
            src_path,
            # grammar_path,
            VSM_path,
            # sql_connector,
            derby_path,
            tokenizer: NLP,
            delete_derby_db_after=True,
            project_id=None,
    ) -> int:
        """creates and stores all data needed from source files: tokens and vsm indexes

        Args:
            src_path (str): path to source files
            grammar_path (str): path to grammar directory
            VSM_path (str): path to store vsm data
            sql_connector (SqlConnector):
            derby_path (str): directory to store derby data in
            delete_derby_db_after (bool): whether to delete the derby data after parsing
            project_id (int, optional): . Defaults to None.

        Returns:
            list: collection of source file objects parsed
        """
        # clean database before indexing
        self.sql_connector.clean_db()

        num_of_parsed_files = self.parse_and_store_src_tokens_with_jim(
            src_path=src_path,
            # grammar_path=grammar_path,
            # sql_connector=sql_connector,
            derby_path=derby_path,
            delete_derby_db_after=delete_derby_db_after,
            tokenizer=tokenizer,
            project_id=project_id,
        )

        src_files = self.sql_connector.get_src_files()

        create_vsm_indexes(VSM_path, src_files, project_id)

        return src_files


def create_vsm_indexes(VSM_path, src_files, project_id):
    """creates vsm indexes

    Args:
        VSM_path (str): path to store vsm data
        src_files (list): collection of db src file objects
        project_id (int):
    """
    logger.info("Creating VSM indexes")

    # this VSM instance will have index information which we don't need to keep
    VSM(VSM_path, project_id).index_src_files(src_files)
