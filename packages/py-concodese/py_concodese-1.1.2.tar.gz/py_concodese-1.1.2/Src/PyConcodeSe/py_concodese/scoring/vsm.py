"""
Based roughly on
src/main/java/de/dilshener/concodese/term/search/lucene/ComponentWordsIndexer.java
"""
from __future__ import annotations
from jpype import JClass
from os.path import join, isdir
from shutil import rmtree
import logging


from py_concodese.storage.filebase import TermTypes

logger = logging.getLogger(__name__)

INDEX_NAME_BASE = ".temp_index"


class VSM:
    def __init__(self, vsm_path, project_id=None, test=False) -> None:
        self.lucene_version = JClass("org.apache.lucene.util.Version").LUCENE_36
        self.vsm_path = vsm_path
        self.project_id = project_id
        self.test = test

        self.index_writers = {}  # (stemmed, comments) -> index_writer class
        self.index_searchers = {}  # (stemmed, comments) -> index_searcher class

        self.prepared_queries = {}  # (BReport, stemmed) -> query class

        self.use_precached_results = False

    def release_JClass_objects(self):
        """JClass objects are unpicklable so if you don't need them anymore
        clear them away to make this object work as a multiprocessing arg
        """
        self.lucene_version = None
        self.index_writers = None
        self.index_searchers = None
        self.prepared_queries = None

    def precache_vsm_ranks(self, bug_reports, release_JClass_objects=True):
        """calculates vsm ranks for bug reports and stores them in the class"""
        self.vsm_file_ranks_and_scores = {}

        for bug_report in bug_reports:
            for comments in [False, True]:
                for stemmed in [False, True]:
                    # order is unstemmed/code, stemmed/code, unstemmed/all, stemmed/all
                    self.vsm_file_ranks_and_scores[
                        (bug_report, stemmed, comments)
                    ] = self.calc_vsm_ranks_and_scores(bug_report, stemmed, comments)

        # now the results are calculated and stored, we do not have to
        # recalculate them later
        self.use_precached_results = True

        if release_JClass_objects:
            self.release_JClass_objects()

    def get_vsm_ranks_and_scores(
        self, bug_report, stemmed, comments
    ) -> tuple[dict[str, int], dict[str, float]]:
        """get ranks and scores already calculated

        Args:
            bug_report (BugReport): the bug report object to score against
            stemmed (bool): whether to use stemmed terms
            comments (bool): whether to include comments in scoring

        Returns:
            tuple[dict[str, int], dict[str, float]]: tuple of dictionaries.
            First dictionary maps class name to rank.
            Second dictionary maps class name to score.
        """
        return self.vsm_file_ranks_and_scores[(bug_report, stemmed, comments)]

    def get_index_writer(self, stemmed, comments) -> JClass:
        """returns a lucene vsm index writer

        Args:
            stemmed (bool): whether to use stemmed tokens
            comments (bool): whether to include comments

        Returns:
            JClass: An index writer
        """
        # check if requested index writer is already available
        index_writer = self.index_writers.get((stemmed, comments), False)
        if index_writer:
            return index_writer

        fs_dir = JClass("org.apache.lucene.store.FSDirectory").open(
            JClass("java.io.File")(
                VSM.get_index_path(
                    self.project_id,
                    self.vsm_path,
                    stemmed,
                    comments,
                    self.test,
                )
            )
        )

        standard_analyzer = JClass(
            "org.apache.lucene.analysis.standard.StandardAnalyzer"
        )(self.lucene_version)

        iw_conf = JClass("org.apache.lucene.index.IndexWriterConfig")(
            self.lucene_version, standard_analyzer
        ).setOpenMode(
            JClass("org.apache.lucene.index.IndexWriterConfig.OpenMode").CREATE
        )
        # concodese original sets a deletion policy too, but that deletion policy
        # is default anyway, so we don't need to add it

        mp = iw_conf.getMergePolicy()
        mp.setUseCompoundFile(True)
        iw_conf.setMergePolicy(mp)

        index_writer = JClass("org.apache.lucene.index.IndexWriter")(fs_dir, iw_conf)

        mp.close()

        # cache for later
        self.index_writers[(stemmed, comments)] = index_writer

        return index_writer

    def index_src_files(self, src_files: list) -> None:
        """creates vsm indexes for src files

        Args:
            src_files (list): [db File object, ...]
        """

        n = 1
        for comments in [False, True]:
            for stemmed in [False, True]:
                # order is unstemmed/code, stemmed/code, unstemmed/all, stemmed/all

                index_writer = self.get_index_writer(stemmed, comments)

                logger.info(f"Creating VSM index {n}/4 for files 1/{len(src_files)}")

                for idx, src_file in enumerate(src_files):
                    if (idx + 1) % 250 == 0:
                        logger.info(
                            f"Creating VSM index {n}/4 for files {idx+1}/{len(src_files)}"
                        )
                    self.index_src_file(index_writer, src_file, stemmed, comments)

                # optimises index for searching
                index_writer.forceMerge(1, True)

                # commits all changes and closes
                index_writer.close()

                logger.info(f"Created VSM index {n}/4")
                n += 1

    def get_src_file_terms(self, src_file, stemmed, comments) -> set[str]:
        """_summary_

        Args:
            src_file (File model| modeless file):
            stemmed (bool): whether to stem the terms
            comments (bool): whether to include comment terms

        Returns:
            set[str]:
        """
        # DB. i don't know why this is written like this,
        # but I'm not going to risk changing it right now
        get_term_set = src_file.get_term_set
        terms = None
        if not comments:
            terms = get_term_set(TermTypes.code_token, stemmed)
        if comments:
            terms = get_term_set(TermTypes.code_and_comments, stemmed)

        return terms

    def index_src_file(self, index_writer, src_file, stemmed, comments):
        """creates an index for an individual src file

        Args:
            index_writer (JClass):
            src_file ():
            stemmed (bool): whether to stem the terms
            comments (bool): whether to include comment terms
        """
        doc = JClass("org.apache.lucene.document.Document")()

        # add the class field
        klazz_field = JClass("org.apache.lucene.document.Field")(
            "klazz",
            src_file.name_with_ext,
            JClass("org.apache.lucene.document.Field.Store").YES,
            JClass("org.apache.lucene.document.Field.Index").ANALYZED,
        )

        doc.add(klazz_field)

        # add the word list field as a space delimited string
        # 'hw' or 'hard words' in concodese original
        words = self.get_src_file_terms(src_file, stemmed, comments)

        word_field = JClass("org.apache.lucene.document.Field")(
            "words",
            " ".join(words),
            JClass("org.apache.lucene.document.Field.Store").YES,
            JClass("org.apache.lucene.document.Field.Index").ANALYZED,
            JClass("org.apache.lucene.document.Field.TermVector").YES,
        )

        doc.add(word_field)

        index_writer.addDocument(doc)

    def get_index_searcher(self, stemmed, comments) -> JClass:
        # check for cached object first
        index_searcher = self.index_searchers.get((stemmed, comments), False)
        if index_searcher:
            return index_searcher

        fs_dir = JClass("org.apache.lucene.store.FSDirectory").open(
            JClass("java.io.File")(
                VSM.get_index_path(
                    self.project_id,
                    self.vsm_path,
                    stemmed,
                    comments,
                    self.test,
                )
            )
        )
        index_reader = JClass(
            "org.apache.lucene.index.IndexReader",
        ).open(fs_dir)
        index_searcher = JClass(
            "org.apache.lucene.search.IndexSearcher",
        )(index_reader)

        self.index_searchers[(stemmed, comments)] = index_searcher

        return index_searcher

    def prepare_query(self, bug_report, stemmed) -> JClass:
        """collect relevant bug report terms and return a query parser"""
        # check for cached version
        query = self.prepared_queries.get((bug_report, stemmed), False)
        if query:
            return query

        br_terms = bug_report.get_all_tokens(stemmed)

        standard_analyzer = JClass(
            "org.apache.lucene.analysis.standard.StandardAnalyzer"
        )(self.lucene_version)
        query_parser = JClass("org.apache.lucene.queryParser.QueryParser")(
            self.lucene_version, "words", standard_analyzer
        )
        try:
            query = query_parser.parse(" ".join(br_terms))
        except Exception as ex:
            print(ex)
            print(
                f"Too many query terms in {bug_report.bug_id}."
                f" Making term SET for vsm instead of LIST."
            )
            query = query_parser.parse(" ".join(set(br_terms)))

        self.prepared_queries[(bug_report, stemmed)] = query
        return query

    def calc_and_add_vsm_ranks(self, bug_report, file_rank_datas) -> None:
        """
        Adds vsm scores to file_rank_datas
        Args:
            bug_report - instance of bug report class
            file_rank_datas - a list of file_rank_data instances

        (modifies file_rank_data instances)
        """
        for comments in [False, True]:
            for stemmed in [False, True]:
                # order is unstemmed/code, stemmed/code, unstemmed/all, stemmed/all
                vsm_file_ranks, vsm_file_scores = self.calc_vsm_ranks_and_scores(
                    bug_report, stemmed, comments
                )

                for file_rank_data in file_rank_datas:
                    file_rank_data.append_vsm_rank(
                        vsm_file_ranks.get(file_rank_data.src_file.name_with_ext, 9999)
                    )
                    file_rank_data.append_vsm_score(
                        vsm_file_scores.get(file_rank_data.src_file.name_with_ext, 0)
                    )

    def calc_vsm_ranks_and_scores(
        self, bug_report, stemmed, comments
    ) -> tuple[dict[str, int], dict[str, float]]:
        """returns two dictionaries {class_name -> rank}, {class_name -> score}"""
        if self.use_precached_results:
            return self.get_vsm_ranks_and_scores(bug_report, stemmed, comments)
        index_searcher = self.get_index_searcher(stemmed, comments)
        query_parser = self.prepare_query(bug_report, stemmed)

        vsm_file_ranks = {}
        vsm_file_scores = {}
        top_docs = index_searcher.search(query_parser, 9999)
        for idx, score_doc in enumerate(top_docs.scoreDocs):
            doc = index_searcher.doc(score_doc.doc)
            klazz_name = str(doc.getFieldable("klazz").stringValue())
            vsm_file_ranks[klazz_name] = idx + 1
            vsm_file_scores[klazz_name] = score_doc.score

        return vsm_file_ranks, vsm_file_scores

    @staticmethod
    def delete_index_folders(project_id, vsm_path, test) -> None:
        """deletes vsm index data

        Args:
            project_id (int):
            vsm_path (str):
            test (bool): whether to delete test or live vsm data
        """
        for comments in [False, True]:
            for stemmed in [False, True]:
                # order is unstemmed/code, stemmed/code, unstemmed/all, stemmed/all
                index_folder = VSM.get_index_path(
                    project_id,
                    vsm_path,
                    stemmed,
                    comments,
                    test,
                )
                if isdir(index_folder):
                    rmtree(index_folder)

    @staticmethod
    def get_index_path(project_id, vsm_path, stemmed, comments, test) -> str:
        """creates a unique index directory string to keep indexes with
        different parameters separate"""
        return (
            f"{join(vsm_path, INDEX_NAME_BASE)}"
            f"{project_id if project_id is not None else ''}"
            f"{'_test_' if test else ''}"
            f"_{'not_' if not stemmed else ''}"
            f"stemmed"
            f"_{'not_' if not comments else ''}"
            f"comments"
        )
