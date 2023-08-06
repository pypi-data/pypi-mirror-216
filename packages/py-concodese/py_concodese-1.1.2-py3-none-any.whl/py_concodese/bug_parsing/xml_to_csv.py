"""
This script converts xml bug repositories to a csv format accepted by
java-concodese. It can be run stand-alone from the py-concodese application.

call the script using:

python xml_to_csv.py "/full path/to/xmlfile.xml"
"""

import csv
from sys import argv
import xml.etree.ElementTree as ET
import csv
from pathlib import Path
from os.path import join
import re

CLASS_FILE_PATTERN = "[^\/\.]+\.[a-zA-Z]+$"

CSV_COLUMNS = [
    "Key",
    "Summary",
    "Description",
    "Issue Type",
    "Project artefacts effected",
]


def convert(input_file_path):
    input_file = Path(input_file_path)
    if input_file.suffix not in (".xml", ".XML"):
        print("target file must be xml format with an .xml suffix")
        return

    output_file = join(f"{input_file.parent}", f"{input_file.stem}.csv")
    print(f"converting: {input_file} to {output_file}")

    # create new csv file
    with open(
        output_file,
        "w",
        newline="",
    ) as csvfile:

        csv_writer = csv.DictWriter(
            csvfile,
            fieldnames=CSV_COLUMNS,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
        )

        csv_writer.writeheader()

        class_re = re.compile(CLASS_FILE_PATTERN)

        tree = ET.parse(input_file_path)
        for child in tree.getroot():
            # each file needs the path/ package stripped so it's ClassName.ext
            fixed_files = [
                class_re.search(f.text).group(0)
                for f in child.find("fixedFiles").findall("file")
            ]

            csv_writer.writerow(
                {
                    "Key": child.attrib["id"],
                    "Summary": child.find("buginformation").find("summary").text,
                    "Description": child.find("buginformation")
                    .find("description")
                    .text,
                    "Issue Type": "Defect",
                    "Project artefacts effected": ", ".join(fixed_files),
                }
            )


if __name__ == "__main__":

    # get
    if len(argv) < 2:
        print("no file path given as argument")
    else:
        convert(argv[1])
