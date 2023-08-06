from __future__ import annotations
import xml.etree.ElementTree as ET
import logging
import re
import json
from pathlib import Path
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class_name_pattern = "([A-Z]{1}[a-zA-Z0-9_0-9]*)"

# (For Java) matches the intro to a stack trace up until the first " at " before package.module.class.method etc.
# (For C++) matches the intro to a stack trace up until the first " at " before package.module.class.method etc.
stack_intro_pattern = "!(ENTRY|MESSAGE|STACK).+?(?=!|\sat\s)"

# stack_pattern = "at ((?:(?:[\d\w]*\.)*[\d\w]*))\.([\d\w\$]*)\.([\d\w\$]*)\s*\((?:(?:([\d\w]*\.(java|groovy)):(\d*))|([\d\w\s]*))\)"
stack_pattern = "at [^java\.|^sun\.]([a-z]+\.)*([A-Z]{1}[a-zA-Z0-9_0-9]*)(\$[A-Za-z0-9]*)?\.([A-Za-z0-9\_]*)\((([A-Z]{1}[a-zA-Z0-9_0-9]*\.java)\:[\d+]*)?(Unknown Source)?(Native Method)?\)"


class BReport:
    """A class to hold a bug report"""

    def __init__(
        self, bug_id, summary, description, fixed_files, lucene_helper, inc_dup_terms
    ) -> None:
        """
        Args:
            bug_id ([type])
            summary ([type])
            description ([type])
            fixed_files (list): list of files requiring changes to fix bug
            lucene_helper ([type])
            inc_dup_terms (bool): include duplicate terms in the token lists
        """
        self.bug_id = bug_id

        # dictionaries initialised have two keys: False, True
        # these bools refer to the stemmed state of the tokens
        # bool -> []

        # words from the summary in certain positions
        self._key_position_words = {}
        self.set_key_position_words(summary, lucene_helper)

        # extract stack trace class names from the description if present
        self._stack_trace_classes = {}
        self.set_st_classes(description, lucene_helper)

        # if stack trace was found, remove it from desc
        # JAVA CONCODESE DOES NOT REMOVE STACK TRACE FROM DESC TOKENS
        # if len(self._stack_trace_classes[False]) > 0:
        #     description = re.sub(stack_intro_pattern, "", description)
        #     description = re.sub(stack_pattern, "", description)

        # tokens from summary and description
        self._summary_tokens = {}
        self._description_tokens = {}
        self._all_tokens = {}
        self.set_tokens(self._summary_tokens, summary, lucene_helper, inc_dup_terms)
        self.set_tokens(
            self._description_tokens, description, lucene_helper, inc_dup_terms
        )
        self.set_tokens(
            self._all_tokens, f"{summary} {description}", lucene_helper, inc_dup_terms
        )

        # files that were fixed in this BR
        self.fixed_files = fixed_files

        self.summary = summary
        self.description = description

    def __str__(self) -> str:
        return str(
            (
                f"{self.bug_id if self.bug_id else ''}",
                f"summary={self.summary}",
                f"description={self.description}",
                f"fixed_files={self.fixed_files}",
                f"trace_classes={self._stack_trace_classes}",
            )
        )

    def __hash__(self) -> int:
        return hash(self.bug_id)

    def to_json_for_translation(self):

        return {
            # Prepend id_ to avoid the xml converter to prepend 'n' when the id is purely numerical
            # The converter does that to make a valid xml tag
            f"{ 'id_'+self.bug_id if self.bug_id else ''}":
                {"summary": self.summary,
                 "description": self.description
                 }
        }

    def get_kp_words(self, stemmed) -> list[str]:
        return self._key_position_words[stemmed]

    def set_key_position_words(self, summary, lucene_helper) -> list[str]:
        """Uses the untokenized summary words to set the key position words used in lexical scoring
        src/main/java/de/dilshener/concodese/term/search/impl/ConceptPrecisionSearchImpl.java
        The list is assigned in the order: first, second, penult, final.
        """
        # split on common punctuation and spaces (but not full stop)
        summary_words = re.split("\-|,|\!|\?| ", summary)
        # filter out any 'words' that don't contain any letters
        filter_object = filter(lambda x: re.search("\w", x), summary_words)
        summary_words = list(filter_object)

        regex_class_name = BReport.compile_class_name_regex()

        key_position_words = []
        if len(summary_words) > 0:
            key_position_words.append(
                BReport.extract_class_name(summary_words[0], regex_class_name)
            )

        if len(summary_words) > 1:
            key_position_words.append(
                BReport.extract_class_name(summary_words[1], regex_class_name)
            )
            key_position_words.append(
                BReport.extract_class_name(summary_words[-2], regex_class_name)
            )
            key_position_words.append(
                BReport.extract_class_name(summary_words[-1], regex_class_name)
            )

        # lower case and strip out any leading or trailing full stops
        # (other punctuation will have been removed earlier)
        key_position_words = [word.lower().strip(".") for word in key_position_words]
        key_position_words = [word.lower() for word in key_position_words]

        self._key_position_words[False] = key_position_words
        self._key_position_words[True] = lucene_helper.stem_tokens(key_position_words)

    def get_st_classes(self, stemmed) -> list[str]:
        return self._stack_trace_classes[stemmed]

    def set_st_classes(self, description, lucene_helper):
        """extracts and stores the first 4 class names from the stack trace
        which aren't in the standard libraries"""
        class_names = []

        reg_stack = re.compile(stack_pattern)
        reg_class_name = re.compile(class_name_pattern)
        matches = reg_stack.finditer(description)
        for m in matches:
            str_containing_class = m.group(0)

            if not str_containing_class.startswith(
                ("at java.", "at sun.", "at groovy.")
            ):
                class_name = reg_class_name.search(str_containing_class).group(0)

                # order is important so can't use set
                if class_name not in class_names:
                    class_names.append(class_name)

            # only score the first 4
            if len(class_names) >= 4:
                break

        class_names = [class_name.lower() for class_name in class_names]
        self._stack_trace_classes[False] = class_names
        self._stack_trace_classes[True] = lucene_helper.stem_tokens(class_names)

    def get_summary_tokens(self, stemmed) -> list[str]:
        """returns an alphabetically sorted list of tokens"""
        return self._summary_tokens[stemmed]

    def get_description_tokens(self, stemmed) -> list[str]:
        """returns an alphabetically sorted list of tokens"""
        return self._description_tokens[stemmed]

    def get_all_tokens(self, stemmed) -> list[str]:
        """returns an alphabetically sorted list of tokens"""
        return self._all_tokens[stemmed]

    @staticmethod
    def set_tokens(dict, text, lucene_helper, include_duplicates):
        """adds stemmed and unstemmed tokens from the text to the dict
        See:
        src/main/java/de/dilshener/concodese/term/extract/impl/
        ChangeRequestCSVExtractorImpl.java

        In the original, a TreeSet object is used to store words, which
        is ordered:

        "according to the natural ordering of its elements.
        All elements inserted into the set must implement the Comparable
        interface."
        """
        # get tokens from text string
        tokens = lucene_helper.tokenize_string(text)
        lower_tokens = [token.lower() for token in tokens]

        if not include_duplicates:
            # remove duplicates but keep as list type
            lower_tokens = list(set(lower_tokens))

        # sort for consistent order
        lower_tokens.sort()

        dict[False] = lower_tokens
        # if two tokens have the same stem, the stemmed list will
        # include duplicates even if include_duplicates is False
        dict[True] = lucene_helper.stem_tokens(lower_tokens)

    @staticmethod
    def compile_class_name_regex():
        return re.compile(class_name_pattern)

    @staticmethod
    def extract_class_name(word, reg_class_name):
        """extracts a class name or returns the original string"""
        matches = reg_class_name.finditer(word)
        for match in matches:
            return match.group()
        return word


def parse_bug_repository(
    file_path, lucene_helper, inc_dup_terms, max_size=None
) -> list[BReport]:
    """parses a bug repository

    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Raises:
        ValueError: if file extension is not valid

    Returns:
        list[BReport]:
    """

    logger.info("Reading bug repository file")

    ext = Path(file_path).suffix.lower()

    if ext == ".xml":
        bug_reports = parse_xml_bug_repository(
            file_path, lucene_helper, inc_dup_terms, max_size=max_size
        )
    elif ext == ".json":
        bug_reports = parse_json_bug_repository(
            file_path, lucene_helper, inc_dup_terms, max_size=max_size
        )
    else:
        raise ValueError(
            "Invalid bug repository file type. Must be xml, or json and have a matching file extension."
        )

    logger.info(f"{len(bug_reports)} valid bug reports found")

    return bug_reports


def parse_xml_bug_repository(
    file_path, lucene_helper, inc_dup_terms, max_size=None
) -> list[BReport]:
    """parses an xml bug repository
    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Returns:
        list[BReport]:
    """
    tree = ET.parse(file_path)

    bug_reports = []

    for child in tree.getroot():
        if max_size is not None and len(bug_reports) == max_size:
            break

        summary = child.find("buginformation").find("summary").text
        description = child.find("buginformation").find("description").text
        fixed_files = [f.text for f in child.find("fixedFiles").findall("file")]

        start = time.time()
        br = BReport(
            bug_id=child.attrib["id"],
            summary=summary if summary is not None else "",
            description=description if description is not None else "",
            fixed_files=fixed_files if len(fixed_files) > 0 else [],
            lucene_helper=lucene_helper,
            inc_dup_terms=inc_dup_terms,
        )
        end = time.time()
        print(f"Bug report {br.bug_id} parsed in: {end - start} seconds")
        bug_reports.append(br)

    return bug_reports


def parse_json_bug_repository(
    file_path,
    lucene_helper,
    inc_dup_terms,
    max_size=None,
) -> list[BReport]:
    """parses a json bug repository
    Args:
        file_path (str): path to bug repo file
        lucene_helper ():
        inc_dup_terms (bool): if false, duplicate terms from the description/
        summary will be removed from the tokens list.
        max_size (int, optional): if provided, will stop reading bug reports
        when max_size is reached and return current list. Defaults to None.

    Returns:
        list[BReport]:
    """
    ff_ext = (".c", ".cpp", ".rs")

    with open(file_path) as f:
        data = json.load(f)

    bug_reports = []
    value = []
    uselessbugs = 0
    usefulbugs = 0

    for closed_issue in data["closed_issues"].values():
        if max_size is not None and len(bug_reports) == max_size:
            break

        value = closed_issue["files_changed"]
        if value == []:
            uselessbugs = uselessbugs + 1
            continue

        summary = closed_issue["issue_summary"]
        description = closed_issue["issue_description"]

        # we are aware of two datastructures used,
        # 1. a list of two items [#id, file]
        # 2. a list of four items [#id, file, \u2192, file]
        # (there is sometimes repetition of files)
        fixed_files = set()
        for data in closed_issue["files_changed"]:
            for item in data:
                if "." in item:
                    fixed_files.add(item)

        if len(ff_ext) > 0 and not any(
            [fixed_file.endswith(ff_ext) for fixed_file in fixed_files]
        ):
            uselessbugs = uselessbugs + 1
            continue

        usefulbugs = usefulbugs + 1
        bug_id_withhash = closed_issue["issue_id"]

        br = BReport(
            bug_id=bug_id_withhash.replace("#", ""),
            summary=summary if summary is not None else "",
            description=description if description is not None else "",
            fixed_files=list(fixed_files) if len(fixed_files) > 0 else [],
            lucene_helper=lucene_helper,
            inc_dup_terms=inc_dup_terms,
        )
        bug_reports.append(br)

    # print("Total number of usable bugs:", uselessbugs)
    # print("Total number of unusable bugs:", usefulbugs)
    return bug_reports

