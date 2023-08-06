""" A module that implements the scoring algorithms
1. Full terms from the BR and from the file's code.
2. Full terms from the BR and the file's code and comments.
3. Stemmed terms from the BR and the file's code.
4. Stemmed terms from the BR, the file's code and comments.
It is based on the original implementation here at
src/main/java/de/dilshener/concodese/term/search/impl/ConceptPrecisionSearchImpl.java
"""

from __future__ import annotations

from py_concodese.storage.filebase import TermTypes
from .file_rank_data import FileRankData
from decimal import Decimal


def create_src_file_rank_data(bug_report, src_files) -> list[FileRankData]:
    """
    Args:
        bug_report (_type_): instance of bug report class
        src_files (_type_): [db File object, ...]

    Returns:
        list[FileRankData]:
    """
    file_rank_datas = calc_lex_sim_scores_of_src_files(bug_report, src_files)
    FileRankData.set_lex_sim_ranks_from_scores(file_rank_datas)
    return file_rank_datas


def calc_lex_sim_scores_of_src_files(bug_report, src_files) -> list[FileRankData]:
    """calculates lexical similarity scores of every src file for the given
    bug report.

    Args:
        bug_report (BugReport):
        src_files (list):

    Returns:
        list[FileRankData]:
    """
    # get the float scores for src each file
    file_rank_datas = []
    for src_file in src_files:
        file_rank_data = FileRankData(src_file)
        file_rank_data.set_textual_scores(
            calc_lex_sim_scores_of_src_file(bug_report, src_file)
        )
        file_rank_datas.append(file_rank_data)
    return file_rank_datas


def calc_lex_sim_scores_of_src_file(bug_report, src_file) -> list[Decimal]:
    """calculates the 4 lexical similarity scores for a single src file

    Args:
        bug_report (BugReport):
        src_file:

    Returns:
        list[Decimal]: 4 scores
    """
    scores = []
    for comments in [False, True]:
        for stemmed in [False, True]:
            # order is unstemmed/code, stemmed/code, unstemmed/all, stemmed/all
            scores.append(
                lexical_similarity_scoring(bug_report, src_file, stemmed, comments)
            )

    return scores


def lexical_similarity_scoring(bug_report, src_file, stemmed, comments) -> Decimal:
    """get the score of a src file, scoring with the given parameters

    Args:
        bug_report ():
        src_file ():
        stemmed (bool): use stemmed identifiers?
        comments (bool): include comment tokens

    Returns:
        Decimal: a score
    """
    if stemmed:
        file_name = src_file.stemmed_name.lower()
    else:
        file_name = src_file.name.lower()

    # check the summary for key position words that match the file name
    file_score = score_with_key_position_word(
        file_name,
        bug_report.get_kp_words(stemmed),
    )
    # check the stack trace for words that match the file name
    if file_score == 0:
        file_score = score_with_stack_trace(
            file_name, bug_report.get_st_classes(stemmed)
        )

    # do a full file term search
    if file_score == 0:
        if comments:
            term_type = TermTypes.code_and_comments
        else:
            term_type = TermTypes.code_token

        file_score = score_with_file_terms(
            file_name,
            src_file.get_term_set(term_type, stemmed),
            bug_report.get_all_tokens(stemmed),
        )

    return file_score


KEY_POSITION_SCORE_1ST = Decimal("10")
KEY_POSITION_SCORE_2ND = Decimal("8")
KEY_POSITION_SCORE_PENULT = Decimal("6")
KEY_POSITION_SCORE_FINAL = Decimal("4")


def score_with_key_position_word(file_name, key_position_words) -> int:
    """
    Check for class/ file name in summary key positions
    assign corresponding score for: first, second, pen, last
    positions.
    If using stemmed tokens then use the stem of class name
    key_position_words - list
    """

    if len(key_position_words) > 0 and key_position_words[0] == file_name:
        return KEY_POSITION_SCORE_1ST

    if len(key_position_words) > 1 and key_position_words[1] == file_name:
        return KEY_POSITION_SCORE_2ND

    if len(key_position_words) > 3 and key_position_words[-2] == file_name:
        return KEY_POSITION_SCORE_PENULT

    if len(key_position_words) > 2 and key_position_words[-1] == file_name:
        return KEY_POSITION_SCORE_FINAL

    return Decimal("0")


STACK_TRACE_SCORE_1 = Decimal("9")
STACK_TRACE_SCORE_2 = Decimal("7")
STACK_TRACE_SCORE_3 = Decimal("5")
STACK_TRACE_SCORE_4 = Decimal("3")


def score_with_stack_trace(file_name, stack_trace_classes) -> Decimal:
    """
    returns a score if the file class is contained in the stack trace
    """
    zero = Decimal("0")

    if len(stack_trace_classes) < 1:
        return zero

    if file_name == stack_trace_classes[0]:
        return STACK_TRACE_SCORE_1

    if len(stack_trace_classes) < 2:
        return zero

    if file_name == stack_trace_classes[1]:
        return STACK_TRACE_SCORE_2

    if len(stack_trace_classes) < 3:
        return zero

    if file_name == stack_trace_classes[2]:
        return STACK_TRACE_SCORE_3

    if len(stack_trace_classes) < 4:
        return zero

    if file_name == stack_trace_classes[3]:
        return STACK_TRACE_SCORE_4

    return Decimal("0")


FILE_TERMS_SCORE_TERM_IS_FILE_NAME = Decimal("2")
FILE_TERMS_SCORE_TERM_IN_FILE_NAME = Decimal("0.025")
FILE_TERMS_SCORE_TERM_IN_SOURCE = Decimal("0.0125")


def score_with_file_terms(file_name, src_token_set, bug_report_tokens) -> Decimal:
    """ Tezcan's main scoring algorithm. Recreated from Java-ccdse source code:
    1. Checks if a bug report matches the src file name.
    2. Checks if a bug report token appears in the src token set.
    3. Checks if bug report token is within any src code token. (May seem
    strange, and counter to the published algorithm, but this is what happens
    in the java-ccdse source).

    Args:
        file_name (str):
        src_token_set (set[str]):
        bug_report_tokens (list[str]):

    Returns:
        Decimal:
    """

    score = Decimal("0")

    for br_word in bug_report_tokens:
        if br_word == file_name:
            score += FILE_TERMS_SCORE_TERM_IS_FILE_NAME
            # break  # stop scoring
        elif br_word in file_name:
            score += FILE_TERMS_SCORE_TERM_IN_FILE_NAME
        else:
            for src_token in src_token_set:
                if br_word in src_token:
                    score += FILE_TERMS_SCORE_TERM_IN_SOURCE

    return score


def check_for_br_term_in_src(br_word, src_token_set) -> bool:
    """ returns true if a br_word is found in the src """
    if br_word in src_token_set:
        return True
    return False
