from pathlib import Path
from .path_type import PathType, calc_path_type
from py_concodese.scoring.file_rank_data import FileRankData


def top_k(fixed_files, file_rank_datas, k) -> bool:
    """returns true if any top k ranked file appears in the fixed files

    Args:
        fixed_files (list[str]): list of file paths or class paths, given in
        the bug repository.
        file_rank_datas (list[FileRankData]):
        k (int):

    Returns:
        bool:
    """

    assert len(fixed_files) > 0

    # determine whether the fixed files are given as namespace paths or file paths
    path_type = calc_path_type(fixed_files[0])

    # creates a list of the top k files recommended by concodese,
    # in a format that matches the given fixed files
    if path_type == PathType.RELATIVE:
        top_k_file_paths = tuple(
            [str(Path(frd.src_file.relative_file_path)) for frd in file_rank_datas[:k]]
        )
        for fixed_file in fixed_files:
            if str(Path(fixed_file)) in top_k_file_paths:
                return True
    else:
        top_k_file_paths = tuple(
            [frd.src_file.namespace_path for frd in file_rank_datas[:k]]
        )
        for fixed_file in fixed_files:
            if fixed_file in top_k_file_paths:
                return True

    return False


def get_top_k_percent(top_ks) -> float:
    """Calculates the % of True values in a list of booleans.
    Each bool in the list corresponds to a bug report.
    If true, concodese recommended a file in its top k, that was a fixed file.

    Args:
        top_ks (list[bool]):

    Returns:
        float:
    """
    true_count = len([result for result in top_ks if result])
    total_count = len(top_ks)
    return true_count / total_count
