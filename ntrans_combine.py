"""
Reads the .csv files containing N-grams that were generated in ntrans_dataprep.py

Inserts every N-gram into a collections.Counter, to determine the 10K most frequent N-grams of each sorted
(2-grams, 3-grams, etc.).

These N-grams are thereafter written to separate .csv files.
"""

import csv
import collections
import pathlib
from typing import Dict, List, Tuple


NGramCounter = Tuple[str, int]


def delete_chunkfiles() -> None:
    """
    Deletes the generated chunked csv files after the finalized csv files have been finalized.
    """
    confirm = (
        str(
            input(
                "Are you sure you want to delete the chunked data files? This can not be undone. (y/n) "
            )
        )
        .lower()
        .strip()
    )

    path_datachunks = pathlib.Path(("./ngram_data_chunks"))

    if confirm == "y":
        if not path_datachunks.exists():
            print("Cannot find the folder 'ngram_data_chunks'.")
            return
        print("Deleting files ...")
        for file in path_datachunks.glob("*.csv"):
            file.unlink()

        pathlib.Path("./ngram_data_chunks").rmdir()
    elif confirm == "n":
        return
    else:
        print("Please provide a valid input, 'y' or 'n'.")
        delete_chunkfiles()


def write_combined_files(ngram_counter: Dict[int, List[NGramCounter]]) -> None:
    """
    Writes the finalized X most common N-grams to csv-files.
    """
    pathlib.Path("ngrams").mkdir(exist_ok=True)

    for n, collections_counter in ngram_counter.items():
        file_path = f"ngrams/{n}-grams.csv"
        print(f"Writing finalized {n}-gram file")

        with open(file_path, mode="w") as write_ngram_file:
            data_writer = csv.writer(write_ngram_file)

            for ngram, count in collections_counter:
                data_writer.writerow((ngram, count))

    # Warning: Don't uncomment if you still need the chunked files after running the script
    # delete_chunkfiles()


def combine_chunkfiles_into_counter() -> None:
    """
    Reads the chunked csv-files generated in ntrans_dataprep.py and calculates the sum of occurrences
    of each N-gram.
    """

    ngram_counter: Dict[int, List[NGramCounter]] = {
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    path_datachunks = pathlib.Path(("./ngram_data_chunks"))

    if not path_datachunks.exists():
        print(
            """
            Cannot find folder 'ngram_data_chunks'.
            Please make sure that you have run ntrans_dataprep.py to generate
            the chunked data files before running this script.
            """
        )
        return
    for n in ngram_counter:
        ctr: collections.Counter[str] = collections.Counter()
        chunk_files = list(path_datachunks.glob(f"chunk*_{n}-grams.csv"))

        for enum, file in enumerate(chunk_files, start=1):
            print(f"Counting {n}-grams. Currently file {enum}/{len(chunk_files)})")

            with open(file) as ngram_file:
                read_csv = csv.reader(ngram_file)

                for enum, row in enumerate(read_csv):
                    ctr[row[0]] += int(row[1])

        for counted_ngram in ctr.most_common(10000):
            ngram_counter[n].append(counted_ngram)

    write_combined_files(ngram_counter)


combine_chunkfiles_into_counter()
