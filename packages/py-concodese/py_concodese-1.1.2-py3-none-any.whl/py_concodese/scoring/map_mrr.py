"""
Implemented as cited by T:
https://dibt.unimol.it/TAinSM2012/slides/dawn.pdf

In concodese original the map and mrr code is found at
src/main/java/de/dilshener/concodese/term/search/impl/MAPMRRPerformanceComparer.java
and the ranks are always rank + 1. The literature doesn't support this +1 so it's assumed
that the ranks being worked with are 0 based.
This is supported by logic like:

if (rankOfClass == 0){
    top1crs.add(issueKey);
}

which suggests that when the rank is 0, it's included in the top1 results.
"""
from __future__ import annotations

from pathlib import Path

from .path_type import PathType, calc_path_type


def calc_map_and_mrr(fixed_files, file_rank_datas) -> tuple[float, float]:
    """
    returns tuple of: map, mrr
    """

    hit_count = 0
    accumulated_ap = 0
    accumulated_rr = 0

    assert len(fixed_files) > 0

    path_type = calc_path_type(fixed_files[0])

    found_files = set()

    # Transform fixed files identification into platform independent paths
    if path_type != PathType.NAMESPACE:
        fixed_files = [str(Path(fixed_file)) for fixed_file in fixed_files]

    # iterate through all the src files in ranked order
    for frd in file_rank_datas:
        if path_type == PathType.NAMESPACE:
            src_file_path = frd.src_file.namespace_path
        else:
            src_file_path = str(Path(frd.src_file.relative_file_path))

        # if a ranked file matches a fixed file
        for fixed_file in fixed_files:
            if fixed_file in found_files:  # already matched
                continue

            if fixed_file.endswith(src_file_path):
                hit_count += 1
                accumulated_ap += hit_count / frd.overall_rank
                accumulated_rr += 1 / frd.overall_rank

                found_files.add(fixed_file)
                break

        if len(fixed_files) == len(found_files):
            break  # if no more fixed files to be found

    # TODO later this should be a more serious error
    if len(fixed_files) != len(found_files):
        print("Not all fixed files were found in the src")

    if hit_count > 0:
        m_ap = accumulated_ap / hit_count
        m_rr = accumulated_rr / hit_count
    else:
        m_ap = 0
        m_rr = 0

    return m_ap, m_rr
