from pathlib import Path
import os

class FileRankData:
    """A class to handle a file's scores and ranks"""

    def __init__(self, src_file) -> None:
        self.src_file = src_file

        # textual/ lexical similarity
        self._textual_scores = []
        self._textual_ranks = [99999, 99999, 99999, 99999]

        self._vsm_ranks = []
        self._vsm_scores = []

        # final rank based on the ranks of the 8 methods
        self.overall_rank = None

    def __str__(self) -> str:
        return self.get_sortable_ranks()

    def __hash__(self) -> int:
        return hash(self.src_file)

    def __eq__(self, other) -> bool:
        if other.src_file == self.src_file:
            return True
        return False

    def pretty_print(self):
        print(
            f"#{self.overall_rank}\t{self.src_file.name_with_ext}"
            f"\t({self.src_file.package})\t{self._textual_ranks}"
            f"\t{self._vsm_ranks}"
            f"\t{self.get_sortable_ranks()}"
        )

    def set_textual_scores(self, scores) -> None:
        """set textual scores"""
        self._textual_scores = scores

    def set_default_idx(self, default_idx) -> None:
        """sets the default col to be returned by other methods"""
        self.default_idx = default_idx

    def get_textual_score(self, idx=None) -> int:
        """gets an individual score"""
        if idx is None:
            return self._textual_scores[self.default_idx]
        return self._textual_scores[idx]

    def set_textual_rank(self, idx, rank) -> None:
        """sets an individual rank"""
        self._textual_ranks[idx] = rank

    def append_vsm_rank(self, rank) -> None:
        """append the vsm ranks"""
        self._vsm_ranks.append(rank)

    def append_vsm_score(self, rank) -> None:
        """append the vsm score"""
        self._vsm_scores.append(rank)

    def set_overall_rank(self, overall_rank) -> None:
        self.overall_rank = overall_rank

    def get_sortable_ranks(self, use_textual=True, use_vsm=True) -> list:
        """creates a list of sorted (ascending) ranks

        Args:
            use_textual (bool, optional): include textual/ lexical similarity
            ranks? Defaults to True.
            use_vsm (bool, optional): include vsm ranks. Defaults to True.

        Returns:
            list: sorted (ascending) list of ranks, finally appended with the
            src file name. This list can be used to ultimately compare two src
            files to see if one should be ranked above another.
        """
        ranks_to_sort = []
        if use_textual:
            ranks_to_sort += self._textual_ranks
        if use_vsm:
            ranks_to_sort += self._vsm_ranks
        return sorted(ranks_to_sort) + [self.src_file.name_with_ext]

    def get_best_of_ranks_0_based(self) -> int:
        """returns the best rank of any ranking type (0 based)"""
        return min(self._textual_ranks + self._vsm_ranks) - 1

    def get_partial_path(self) -> str:
        """returns a path that only includes parentdir and filename.ext"""
        relative_path = Path(self.src_file.relative_file_path)
        if len(relative_path.parts) > 1:
            return f"{relative_path.parts[-2]}{os.sep}{relative_path.parts[-1]}"
        else:
            return f".{os.sep}{relative_path.parts[-1]}"

    @staticmethod
    def set_lex_sim_ranks_from_scores(file_rank_datas: list):
        """Sets the lexical similarity ranks for each file based on scores.

        Args:
            file_rank_datas (list[FileRankData]):
        """
        # sort the float scores from lex sim to get ranks
        # for each score column, sort descending to get to get the files in order of rank
        for col in range(0, 4):
            # set the default col idx because sort only allows 1 var in their lambda f's
            [fr_data.set_default_idx(col) for fr_data in file_rank_datas]
            # sort by greatest scores first and then alphabetically
            file_rank_datas.sort(
                key=lambda x: (-x.get_textual_score(), x.src_file.name_with_ext)
            )
            # iterate sorted list and set rank of each object
            for idx, file_rank_data in enumerate(file_rank_datas):
                file_rank_data.set_textual_rank(idx=col, rank=idx + 1)

    @staticmethod
    def sort_and_set_overall_rank_of_list(
        file_rank_datas, use_textual=True, use_vsm=True
    ) -> None:
        """Sorts list by comparing ranks for each file, and sets the overall
        rank property for each file.

        Args:
            file_rank_datas (list[FileRankData]): _description_
            use_textual (bool, optional): include textual ranks. Defaults to True.
            use_vsm (bool, optional): include vsm ranks. Defaults to True.
        """
        file_rank_datas.sort(key=lambda x: x.get_sortable_ranks(use_textual, use_vsm))

        for idx, file_rank_data in enumerate(file_rank_datas):
            file_rank_data.set_overall_rank(idx + 1)

    @staticmethod
    def output_all_scores(file_rank_datas):
        """outputs score details for a list of file_rank_datas in a format
        that matches java-concodese.
        Does not change original list order.
        """
        for vsm in [False, True]:
            cs = 0
            for comments in [False, True]:
                for stemmed in [False, True]:
                    print(f"\n isIncludeComments: {comments}, isUseStemWord {stemmed}")
                    # sort by a particular rank
                    sorted_fdr = sorted(
                        file_rank_datas,
                        key=lambda x: (
                            x._vsm_ranks[cs] if vsm else x._textual_ranks[cs]
                        ),
                    )

                    for fdr in sorted_fdr[:10]:
                        print(
                            f"{fdr.src_file.name}: "
                            f"#{fdr._vsm_ranks[cs] if vsm else fdr._textual_ranks[cs]}, "
                            f"{fdr._vsm_scores[cs] if vsm else fdr._textual_scores[cs]}"
                        )
                    cs += 1

    @staticmethod
    def make_tuple_of_partial_paths(file_rank_datas, k):
        """
        k - the number of file_rank_datas to include in the tuple

        returns a tuple containing
        "/parentdir/filename.ext"
        for each file_rank_data
        """
        return tuple(
            [fdr.get_partial_path() for fdr in file_rank_datas[:k]],
        )
