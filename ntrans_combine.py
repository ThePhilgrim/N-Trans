"""
Reads the .csv files containing N-grams that were generated in ntrans_dataprep.py

Inserts every N-gram into a collections.Counter, to determine the 50K most frequent N-grams of each sorted
(2-grams, 3-grams, etc.).

These N-grams are thereafter written to separate .csv files.
"""

import csv
import collections
import glob


def count_ngrams(ngram, count):
    pass


def read_ngram_files():
    """
    Reads the chunked csv-files generated in ntrans_dataprep.py and calculates the sum of occurrences
    of each N-gram.
    """
    # TODO: Update docstring when count_ngrams() works.

    ngram_counter = {
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    for n in range(2, 4):  # "for key in ngram_counter" when test phase is over

        ctr = collections.Counter()
        chunk_files = glob.glob(f"ngram_data_chunks/chunk*_{n}-grams.csv")

        for enum, file in enumerate(chunk_files, start=1):

            print(f"Currently counting {file}. (File {enum}/{len(chunk_files)})")

            with open(file) as ngram_file:

                read_csv = csv.reader(ngram_file)

                for enum, row in enumerate(read_csv):
                    ctr[row[0]] += int(
                        row[1]
                    )  # TODO: Send Counting to separate function

        ngram_counter[n].append(ctr.most_common(5000))
        print(ngram_counter[n])


read_ngram_files()


"""
IMPLEMENTATION NOTES:

for loop 2 - 6 (n for ngram)

    for loop all files 2 grams, then all files 3 grams, etc.

    add all strings to counter

    call write_csv_function(current_counter)

    clear counter

"""
