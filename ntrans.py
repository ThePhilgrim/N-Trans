"""
The usage of this script relies on the N-gram files in "./ngrams"

These files are generated through ntrans_dataprep.py and processed in ntrans_combine.py
"""

import translatepy  # type: ignore
import csv
from typing import List, Dict, Tuple, Any


SourceTarget = Tuple[str, str]


def create_csv_file(
    source_target_pairs: List[SourceTarget], user_choices: Dict[str, Any]
) -> None:
    """
    Writes source/target pairs to a csv-file
    """

    path = (
        user_choices["save_path"] + "/"
    )
    filename = "ntrans-glossary.csv"  # TODO: Make filename depend on user input
    full_path = path + filename

    with open(full_path, mode="w") as write_ntrans_file:
        data_writer = csv.writer(write_ntrans_file, delimiter=",")

        data_writer.writerow(("English", "Swedish"))
        for source_target_pair in source_target_pairs:
            data_writer.writerow(source_target_pair)

    return print("N-Trans CSV Glossary has been successfully saved to " + full_path)


def machine_translate_ngrams(
    ngrams: Dict[int, List[str]], user_choices: Dict[str, Any]
) -> None:
    """
    Translates each N-gram and appends the source/target pair to a list.
    """
    source_target_pairs: List[SourceTarget] = []

    translator = translatepy.Translator()

    for key, value in ngrams.items():
        for enum, source_ngram in enumerate(value, start=1):
            print(f"Translating {key}-gram no. {enum} / {len(value)}")
            target_ngram = str(
                translator.translate(source_ngram, user_choices["target_language"])
            ).lower()  # TODO: Target language should be variable-based
            source_target_pairs.append((source_ngram, target_ngram))

    create_csv_file(source_target_pairs, user_choices)


def read_ngram_files(user_choices: Dict[str, Any]) -> None:
    """
    Reads N-gram files depending on which N-grams the user wants to output.

    Appends the N-grams to a dict with a size of data_size per N-gram (specified by user).
    """

    ngrams: Dict[int, List[str]] = {n: [] for n in user_choices["included_ngrams"]}

    for n in ngrams:
        with open(f"./ngrams/{n}-grams.csv") as ngram_file:
            read_csv = csv.reader(ngram_file)
            for enum, row in enumerate(read_csv):
                if enum == user_choices["amount_of_ngrams"]:
                    break
                ngrams[n].append(row[0])

    machine_translate_ngrams(ngrams, user_choices)


# read_ngram_files()
