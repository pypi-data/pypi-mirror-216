""" A module that implements the scoring algorithms
1. Full terms from the BR and from the file's code.
2. Full terms from the BR and the file's code and comments.
3. Stemmed terms from the BR and the file's code.
4. Stemmed terms from the BR, the file's code and comments.

It extends the original implementation here at
src/main/java/de/dilshener/concodese/term/search/impl/ConceptPrecisionSearchImpl.java

see the wiki article on alternative heuristics for a larger explanation of how this module works.
"""

from __future__ import annotations
from .file_rank_data import FileRankData
from py_concodese.storage.filebase import TermTypes
from decimal import Decimal

ZERO = Decimal("0")


def create_src_file_rank_data(bug_report, src_files, scoring_cfg) -> list[FileRankData]:
    """
    Args:
        bug_report (_type_): instance of bug report class
        src_files (_type_): [db File object, ...]
        scoring_cfg (dict[str -> Decimal]): _description_

    Returns:
        list[FileRankData]:
    """
    file_rank_datas = calc_lex_sim_scores_of_src_files(
        bug_report, src_files, scoring_cfg
    )
    FileRankData.set_lex_sim_ranks_from_scores(file_rank_datas)
    return file_rank_datas


def calc_lex_sim_scores_of_src_files(
    bug_report, src_files, scoring_cfg
) -> list[FileRankData]:
    """calculates lexical similarity scores of every src file for the given
    bug report

    Args:
        bug_report (BugReport):
        src_files (list):
        scoring_cfg (dict):

    Returns:
        list[FileRankData]:
    """
    # get the float scores for src each file
    file_rank_datas = []
    for src_file in src_files:
        file_rank_data = FileRankData(src_file)
        file_rank_data.set_textual_scores(
            calc_lex_sim_scores_of_src_file(bug_report, src_file, scoring_cfg)
        )
        file_rank_datas.append(file_rank_data)
    return file_rank_datas


def calc_lex_sim_scores_of_src_file(bug_report, src_file, scoring_cfg) -> list[Decimal]:
    """calculates the 4 lexical similarity scores for a single src file

    Args:
        bug_report (BugReport):
        src_file:
        scoring_cfg (dict):

    Returns:
        list[Decimal]: 4 scores
    """
    scores = []
    for comments in [False, True]:
        for stemmed in [False, True]:
            # order is unstemmed/code, stemmed/code, unstemmed/all, stemmed/all
            scores.append(
                lexical_similarity_scoring(
                    bug_report, src_file, stemmed, comments, scoring_cfg
                )
            )

    return scores


def lexical_similarity_scoring(
    bug_report, src_file, stemmed, comments, scoring_cfg
) -> Decimal:
    """get the score of a src file, scoring with the given parameters

    Args:
        bug_report ():
        src_file ():
        stemmed (bool): use stemmed identifiers?
        comments (bool): include comment tokens
        scoring_cfg (dict):

    Returns:
        Decimal: a score
    """
    if stemmed:
        file_name = src_file.stemmed_name.lower()
    else:
        file_name = src_file.name.lower()

    # check the summary key position words for similarities with class name
    file_score = score_with_key_position_word(
        file_name, bug_report.get_kp_words(stemmed), scoring_cfg
    )
    # check the stack trace for words that match the file name
    file_score += score_with_stack_trace(
        file_name, bug_report.get_st_classes(stemmed), scoring_cfg
    )

    # score br terms against terms from the file
    file_score += score_all_bug_term(
        bug_report, src_file, stemmed, comments, file_name, scoring_cfg
    )

    return file_score


def score_all_bug_term(
    bug_report, src_file, stemmed, comments, file_name, scoring_cfg
) -> float:
    """returns a cumulative score for all bug report and src file tokens,
    for the given parameters

    Args:
        bug_report:
        src_file:
        stemmed (bool): whether to use stemmed tokens
        comments (bool): whether to include src code comments
        file_name (str): used to make comparisons with bug report tokens,
        stemmed file name may be passed.
        scoring_cfg (dict):

    Returns:
        float: score
    """
    scored_br_terms = set()
    scores = [ZERO]

    identifier_set = src_file.get_term_set(TermTypes.identifier, stemmed)
    code_token_set = src_file.get_term_set(TermTypes.code_token, stemmed)
    comment_token_set = (
        src_file.get_term_set(TermTypes.comment_token, stemmed) if comments else set()
    )
    # score summary terms
    for br_term in bug_report.get_summary_tokens(stemmed):
        score = score_bug_term(
            br_term,
            file_name,
            identifier_set,
            code_token_set,
            comment_token_set,
            scoring_cfg,
        )
        # reduce score if in set of already scored
        if br_term in scored_br_terms:
            score *= 1 - scoring_cfg["RTc"]

        # record that this br term has appeared and we have scored it
        scored_br_terms.add(br_term)
        scores.append(score)

    # score description terms in the same way, except account for "Tc" ***
    for br_term in bug_report.get_description_tokens(stemmed):
        score = score_bug_term(
            br_term,
            file_name,
            identifier_set,
            code_token_set,
            comment_token_set,
            scoring_cfg,
        )
        # reduce score if in set of already scored
        if br_term in scored_br_terms:
            score *= 1 - scoring_cfg["RTc"]

        score *= 1 - scoring_cfg["Tc"]  # ***
        # record that this br term has appeared and we have scored it
        scored_br_terms.add(br_term)
        scores.append(score)

    return sum(scores)


def score_bug_term(
    br_term, file_name, identifier_set, code_token_set, comment_token_set, scoring_cfg
):
    """Returns the score awarded to a bug term before factoring in repeated
    term appearances or whether the term came from a summary or description.

    Args:
        br_term (str): term from bug report
        file_name (str): the src file name/ class name
        identifier_set (set[str]): set of identifiers from src file
        code_token_set (set[str]): set of code tokens from src file
        comment_token_set (set[str]): set of comments from src file
        scoring_cfg (dict): dictionary with scoring parameters

    Returns:
        Decimal: maximum possible score for the term
    """
    possible_scores = []

    # does the term match the file name/ partial match the file name
    if br_term == file_name:
        possible_scores.append(scoring_cfg["CNS"])
    else:
        possible_scores.append(
            (1 - scoring_cfg["Pc"])
            * scoring_cfg["CNS"]
            * find_greatest_partial_match([br_term], file_name)
        )

    if br_term in identifier_set:
        possible_scores.append(scoring_cfg["ITS"])
    if br_term in code_token_set:
        possible_scores.append(scoring_cfg["TTS"])
    if br_term in comment_token_set:
        possible_scores.append(scoring_cfg["CTS"])

    # choose the highest possible score
    return max(possible_scores)


def score_with_key_position_word(file_name, key_position_words, scoring_cfg) -> float:
    """Check for class/ file name in summary key positions. Then check for
    partial matches.

    Args:
        file_name (str): file name string to match with bug report KP words
        key_position_words (list[str]): terms from the bug report to match with
        scoring_cfg (dict):

    Returns:
        float: score (can be zero)
    """
    if file_name in key_position_words:
        return scoring_cfg["KPS"]

    # find partial matches
    partial_value = find_greatest_partial_match(key_position_words, file_name)
    return partial_value * scoring_cfg["KPS"] * (1 - scoring_cfg["Pc"])


def find_greatest_partial_match(term_list, class_name) -> Decimal:
    """compares the class name with every term in the term_list.
    Uses the greatest class name/ term overlap to generate a score.
    returns 0 if no match is made.
    overlaps below 30% are ignored.
    """
    partial_values = []

    # make a list of all the partial overlap values
    for term in term_list:
        partial_value = 0
        if class_name in term:
            partial_value = len(class_name) / len(term)
        elif term in class_name:
            partial_value = len(term) / len(class_name)
        partial_values.append(partial_value)

    # return greatest partial overlap value
    greatest_partial_match = max(partial_values)
    if greatest_partial_match >= 0.3:
        return Decimal(greatest_partial_match)
    return ZERO


def score_with_stack_trace(file_name, stack_trace_classes, scoring_cfg) -> Decimal:
    """returns a score if the file class is contained in the stack trace

    Args:
        file_name (str):
        stack_trace_classes (list[str]):
        scoring_cfg (dict):

    Returns:
        Decimal: score (zero if no match is found)
    """

    for n, st_class_name in enumerate(stack_trace_classes):
        if file_name == st_class_name:
            return scoring_cfg["STS"] * (1 - (n * scoring_cfg["STc"]))

    return ZERO
