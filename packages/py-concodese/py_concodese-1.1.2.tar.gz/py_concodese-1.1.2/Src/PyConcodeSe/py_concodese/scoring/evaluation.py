from os.path import join
from datetime import datetime
import csv
from statistics import mean
from py_concodese.scoring.file_rank_data import FileRankData
from py_concodese.scoring.map_mrr import calc_map_and_mrr
from py_concodese.scoring.top_k import top_k, get_top_k_percent
from py_concodese.scoring.lexical_similarity import create_src_file_rank_data
from py_concodese.scoring.lexical_similarity_orig import (
    create_src_file_rank_data as create_src_file_rank_data_orig,
)
from py_concodese.scoring.bug_result import BugResult, BugResultSummary
from py_concodese.scoring.vsm import VSM
from py_concodese.scoring.path_type import PathType, calc_path_type
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calc_bug_result(
    br, src_files, vsm, alt_lex_sim=False, scoring_cfg=None, showscores=False
) -> BugResult:
    """calculates src file recommendations for a bug, and evaluates the
    recommendations' accuracy based on a bug report's fixed files

    Args:
        br (BugReport):
        src_files (list):
        vsm (VSM):
        alt_lex_sim (bool, optional): whether to use the alternative method of
        lexical similarity scoring. Defaults to False.
        scoring_cfg (dict, optional): required for alternative lex sim scoring.
        Defaults to None.
        showscores (bool, optional): Prints detailed scoring information to
        command line. Defaults to False.

    Returns:
        BugResult: An instance that contains the recommended file data as well
        as evaluation stats.
    """
    if alt_lex_sim:
        file_rank_datas = create_src_file_rank_data(br, src_files, scoring_cfg)
    else:
        file_rank_datas = create_src_file_rank_data_orig(br, src_files)

    vsm.calc_and_add_vsm_ranks(br, file_rank_datas)

    if showscores:
        FileRankData.output_all_scores(file_rank_datas)

    FileRankData.sort_and_set_overall_rank_of_list(file_rank_datas)

    # evaluate top k
    top_1 = top_k(br.fixed_files, file_rank_datas, k=1)
    top_5 = top_k(br.fixed_files, file_rank_datas, k=5)
    top_10 = top_k(br.fixed_files, file_rank_datas, k=10)

    # calc MAP
    m_ap, m_rr = calc_map_and_mrr(br.fixed_files, file_rank_datas)

    result = BugResult(
        bug_report=br,
        top_1=top_1,
        top_5=top_5,
        top_10=top_10,
        m_ap=m_ap,
        m_rr=m_rr,
        top10_frd=file_rank_datas[:10],
    )

    return result


def write_results_to_csv(
    output_path,
    summary: BugResultSummary,
    full_bug_results: list,
):
    """writes a bug result summary to csv

    Args:
        output_path (str): path to save csv
        summary (BugResultSummary): An evaluation/ summary of a whole bug repository,
        is added at the bottom of the file.
        full_bug_results (list[BugResult]): One bug result per evaluated bug.
    """
    with open(
        join(output_path, f"results{str(datetime.now())}.csv"),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = [
            "br_id",
            "top1",
            "top5",
            "top10",
            "map",
            "mrr",
            "heading",
        ]

        csv_writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=",",
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL,
        )

        csv_writer.writeheader()

        for bresult in full_bug_results:
            csv_writer.writerow(
                {
                    "br_id": bresult.bug_report.bug_id,
                    "top1": bresult.top_1,
                    "top5": bresult.top_5,
                    "top10": bresult.top_10,
                    "map": bresult.m_ap,
                    "mrr": bresult.m_rr,
                }
            )
        if summary:
            csv_writer.writerow(
                {
                    "top1": summary.top_1,
                    "top5": summary.top_5,
                    "top10": summary.top_10,
                    "map": summary.m_ap,
                    "mrr": summary.m_rr,
                    "heading": summary.heading,
                }
            )


def write_mulitple_scoring_results_to_csv(csv_output_path, summaries):
    """when pyccdse evaluates the same bug repository using multiple scoring
    methods this method can be used to save the results for all scoring methods

    Args:
        csv_output_path (str): path to save file
        summaries (list[BugReportSummary]):
    """
    with open(
        join(csv_output_path, "results_scoring_cfgs.csv"),
        "w",
        newline="",
    ) as csvfile:
        fieldnames = ["top1", "top5", "top10", "map", "mrr", "heading"]

        csv_writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=",",
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL,
        )

        csv_writer.writeheader()

        for summary in summaries:
            csv_writer.writerow(
                {
                    "top1": summary.top_1,
                    "top5": summary.top_5,
                    "top10": summary.top_10,
                    "map": summary.m_ap,
                    "mrr": summary.m_rr,
                    "heading": summary.heading,
                }
            )


def calc_results_for_all_bug_reports(
    bug_reports,
    src_files,
    scoring_cfg,
    alt_lex_sim,
    vsm=None,
    vsm_path=None,
    print_summary=False,
    summary_to_csv=False,
    full_to_csv=False,
    csv_output_path=None,
) -> BugResultSummary:
    """Evaluates the recommendations made for each bug report

    Args:
        bug_reports (list[BReport]): a list of bug reports to score
        src_files (list[SrcFile]): a list of src files to score
        scoring_cfg (dict): a dictionary containing the score parameters
        alt_lex_sim (bool): whether to use the 'alternative' lexical similarity methods
        vsm (VSM, optional): can be created in function. Defaults to None.
        vsm_path (str, optional): path to store vsm indexes. Defaults to None.
        print_summary (bool, optional): Whether to print summary to console
        summary_to_csv (bool, optional): Save summary to csv. Defaults to False.
        full_to_csv (bool, optional): Icnlude each bug report's result in csv.
        csv_output_path (str, optional): the path to csv files. Defaults to None.

    Returns:
        BugResultSummary
    """
    if len(bug_reports) == 0:
        logger.info(f"No valid bug reports found")
        return

    if vsm is None:
        vsm = VSM(vsm_path)

    logger.info(f"Evaluating performance over {len(bug_reports)} bug reports")

    last_update_time = datetime.now().timestamp()

    bug_results = []
    for idx, br in enumerate(bug_reports):
        # if more than 30s since last update
        if last_update_time + 30 < datetime.now().timestamp():
            logger.info(f"Evaluating performance {idx}/{len(bug_reports)} complete")
            last_update_time = datetime.now().timestamp()
        bug_results.append(
            calc_bug_result(br, src_files, vsm, alt_lex_sim, scoring_cfg)
        )

    summary = BugResultSummary(
        heading="" if scoring_cfg is None else str(scoring_cfg),
        top_1=get_top_k_percent([b_res.top_1 for b_res in bug_results]),
        top_5=get_top_k_percent([b_res.top_5 for b_res in bug_results]),
        top_10=get_top_k_percent([b_res.top_10 for b_res in bug_results]),
        m_ap=mean([b_res.m_ap for b_res in bug_results]),
        m_rr=mean([b_res.m_rr for b_res in bug_results]),
    )

    logger.info(f"Performance evaluation complete")

    if print_summary:
        summary.pretty_print()

    if full_to_csv or summary_to_csv:
        write_results_to_csv(
            output_path=csv_output_path,
            summary=summary if summary_to_csv else None,
            full_bug_results=bug_results if full_to_csv else [],
        )

    return summary


CSV_FIELD_NAMES = ["Cr", "Class Name", "ConCodeSe Rank BestOf"]


def write_incorrect_map_mrr_comparer_csv(bug_reports, src_files, vsm_path, csv_output_path,):
    """creates a csv of evaluation data and implements the same bug as
    java-concodese so that py-ccdse and j-ccdse can be compared. See
    the wiki page on Java-Concodese, subsection "incorrect-evaluation".
    Also relevant is the function "get_incorrectly_normalized_rank".

    Args:
        bug_reports (list[BugReport]):
        src_files (list):
        vsm_path (str):
        csv_output_path (str):
    """

    vsm = VSM(vsm_path)

    # create a file and write header row
    with open(
        join(csv_output_path, "_input_for_map_mrr.csv"),
        "w",
        newline="",
    ) as csvfile:

        csv_writer = csv.DictWriter(
            csvfile,
            fieldnames=CSV_FIELD_NAMES,
            delimiter=";",
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL,
        )

        csv_writer.writeheader()

        for br in bug_reports:
            # calculate the ranks of all src files for a bug report
            file_rank_datas = create_src_file_rank_data_orig(br, src_files)
            vsm.calc_and_add_vsm_ranks(br, file_rank_datas)
            FileRankData.sort_and_set_overall_rank_of_list(file_rank_datas)

            # determine which type of paths are written in the br dataset
            assert len(br.fixed_files) > 0
            path_type = calc_path_type(br.fixed_files[0])

            found_fixed_files = 0
            previous_rank = -1
            normalized_rank = -1
            # iterate through the file rank data looking for the fixed files,
            # highest ranked fixed files will appear first
            for frd in file_rank_datas:
                if path_type == PathType.NAMESPACE:
                    src_file_path = frd.src_file.namespace_path
                else:
                    src_file_path = frd.src_file.relative_file_path

                if src_file_path in br.fixed_files:
                    previous_rank, normalized_rank = get_incorrectly_normalized_rank(
                        file_rank_data=frd,
                        previous_rank=previous_rank,
                        normalized_rank=normalized_rank,
                    )

                    # write data row for fixed file that matches
                    csv_writer.writerow(
                        {
                            "Cr": br.bug_id,
                            "Class Name": f"{frd.src_file.name_with_ext}",
                            "ConCodeSe Rank BestOf": normalized_rank,
                            # "ConCodeSe Rank": 0,
                            # "ConCodeSe Comments": 0,
                            # "ConCodeSe Stems": 0,
                            # "ConCodeSe Comm Stems": 0,
                            # "ConCodeSe VSM": 0,
                            # "ConCodeSe VSM Comm": 0,
                            # "ConCodeSe VSM Stems": 0,
                            # "ConCodeSe VSM Comm Stems": 0,
                            # "Best of CC Rank": 0,
                            # "Best of VSM Rank": 0,
                        }
                    )

                    found_fixed_files += 1
                    if found_fixed_files == len(br.fixed_files):
                        break
            else:
                print("not all fixed files found in source")


def get_incorrectly_normalized_rank(file_rank_data, previous_rank, normalized_rank):
    """this function returns a rank calculated in the same way as
    java-ccdse. It's not the actual rank, it's usually the best rank a file is
    given from any of the 8 categories.

    More generally, it's just a number, and it has no 'real' meaning.
    Don't try to fix/ improve it.
    see ln 306 of /SearchAndRankFilesServiceImpl.java for more info.

    returns:
        a tuple of two ints: (previous_rank, normalized_rank)
    """
    current_rank = file_rank_data.get_best_of_ranks_0_based()
    if current_rank < 10:
        if current_rank == previous_rank:
            normalized_rank += 1
            previous_rank = current_rank
        else:
            if normalized_rank >= current_rank:
                normalized_rank += 1
            else:
                normalized_rank = current_rank
            previous_rank = current_rank
    else:
        normalized_rank = file_rank_data.get_best_of_ranks_0_based()

    return previous_rank, normalized_rank


def calc_map_mrr_from_incorrect_csv(csv_output_path):
    """calculates the topk map/ mrr stats from the csv sheet in the same
    way as java-ccdse. Do not try to improve this function as it's
    written in a way that closely matches the logic in java-ccdse.
    see /MAPMRRPerformanceComparer.java ln131 for more details.
    """
    # A dictionary that holds issue keys and the ranks of fixed files
    # issue_key -> set(<int>)
    issue_ranks = {}

    # sets that hold issue keys
    top1crs = set()
    top5crs = set()
    top10crs = set()

    # lists that hold result for each CR
    mean_avrg_p = []
    mean_recip_r = []

    # accumulates through all CRs
    total_ap_of_cr = 0
    total_rr_of_cr = 0

    with open(
        join(csv_output_path, "_input_for_map_mrr.csv"),
        "r",
    ) as csvfile:

        csv_reader = csv.DictReader(
            csvfile,
            delimiter=";",
        )

        for row in csv_reader:
            issue_key = row["Cr"]

            # add issue key to dictionary if this is the first fixed file
            if issue_key not in issue_ranks:
                issue_ranks[issue_key] = set()

            rank_of_class = int(row["ConCodeSe Rank BestOf"])
            # add 'rank' to the set for this issue key
            issue_ranks[issue_key].add(rank_of_class)

            if rank_of_class == 0:
                top1crs.add(issue_key)
            if rank_of_class < 5:
                top5crs.add(issue_key)
            if rank_of_class < 10:
                top10crs.add(issue_key)

        for issue_key, rank_set in issue_ranks.items():
            # variables to hold various evaluation metrics for an issue
            hit_count_at_top_N = 0
            accumulated_ap = 0.0
            accumulated_rr = 0.0

            # calculate some results for each ranked file
            for rank in rank_set:
                hit_count_at_top_N += 1
                average_precision = hit_count_at_top_N / (rank + 1)
                reciprocal_recall = 1 / (rank + 1)
                accumulated_ap += average_precision
                accumulated_rr += reciprocal_recall

            # store overall ap and rr for CR
            total_ap_of_cr += store_map(accumulated_ap, hit_count_at_top_N, mean_avrg_p)
            total_rr_of_cr += store_mrr(accumulated_rr, mean_recip_r)

        # i don't know why these extra calls would be needed
        # but they're in the original source so i'm just copying
        store_map(accumulated_ap, hit_count_at_top_N, mean_avrg_p)
        store_mrr(accumulated_rr, mean_recip_r)

        # map: Mean Average Precision
        map = total_ap_of_cr / (len(mean_avrg_p) - 1)
        print(
            f"MAP: {map} with #qrySize: {len(mean_avrg_p) - 1} - "
            f"calc.ed as (totalAPofCR: {total_ap_of_cr} / "
            f"#qrySize: {len(mean_avrg_p) - 1})"
        )

        # mrr: mean reciprocal rank
        mrr = total_rr_of_cr / (len(mean_recip_r) - 1)
        print(
            f"MRR: {mrr} with #qrySize: {len(mean_recip_r) - 1} - "
            f"calc.ed as (totalRRofCR: {total_rr_of_cr} / "
            f"#qrySize: {len(mean_recip_r) - 1})"
        )

        print(f"Top1: {len(top1crs)}")
        print(f"Top5: {len(top5crs)}")
        print(f"Top10: {len(top10crs)}")


def store_map(accumulated_ap, hit_count_at_top_N, mean_avrg_p):
    if accumulated_ap > 0:
        total_ap_of_cr = accumulated_ap / hit_count_at_top_N
        mean_avrg_p.append(total_ap_of_cr)
    else:
        mean_avrg_p.append(0.0)
    return total_ap_of_cr


def store_mrr(accumulated_rr, mean_recip_r):
    if accumulated_rr > 0:
        total_rr_of_cr = accumulated_rr
        mean_recip_r.append(total_rr_of_cr)
    else:
        mean_recip_r.append(0.0)
    return total_rr_of_cr
