"""
Reads the .csv files containing N-grams that were generated in ntrans_dataprep.py

Inserts every N-gram into a collections.Counter, to determine the 50K most frequent N-grams of each sorted
(2-grams, 3-grams, etc.).

These N-grams are thereafter written to separate .csv files.
"""

import csv
import collections
import pathlib


def delete_chunkfiles():
    pass


def write_combined_files(ngram_counter):
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


def combine_chunkfiles_into_counter():
    """
    Reads the chunked csv-files generated in ntrans_dataprep.py and calculates the sum of occurrences
    of each N-gram.
    """

    ngram_counter = {
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    for n in ngram_counter:
        ctr = collections.Counter()
        chunk_files = list(pathlib.Path("ngram_data_chunks").glob(f"chunk*_{n}-grams.csv"))

        for enum, file in enumerate(chunk_files, start=1):
            print(f"Counting {n}-grams. Currently file {enum}/{len(chunk_files)})")

            with open(file) as ngram_file:
                read_csv = csv.reader(ngram_file)

                for enum, row in enumerate(read_csv):
                    ctr[row[0]] += int(
                        row[1]
                    )

        for counted_ngram in ctr.most_common(10000):
            ngram_counter[n].append(counted_ngram)

    write_combined_files(ngram_counter)


combine_chunkfiles_into_counter()
