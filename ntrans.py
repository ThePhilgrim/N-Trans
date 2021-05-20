import translatepy
import csv

"""
DEVELOPER INFO:

The usage of this script relies on the N-gram files in "./ngrams"

These files are created through ntrans_dataprep.py
"""


def create_csv_file(source_target_pairs, save_path=None):
    """
    Writes source/target pairs to a csv-file
    """

    path = "/Users/Writing/Desktop/"  # TODO: Make path depend on user input and use "save_path"
    filename = "ntrans-glossary.csv"  # TODO: Make filename depend on user input
    full_path = path + filename

    with open(full_path, mode="w") as write_ntrans_file:
        data_writer = csv.writer(write_ntrans_file, delimiter=",")

        data_writer.writerow(("English", "Swedish"))
        for source_target_pair in source_target_pairs:
            data_writer.writerow(source_target_pair)

    return print("N-Trans CSV Glossary has been successfully saved to " + full_path)


def machine_translate_ngrams(ngrams):
    """
    Translates each N-gram and appends the source/target pair to a list.
    """
    source_target_pairs = []

    translator = translatepy.Translator()

    for n in ngrams.keys():
        for enum, source_ngram in enumerate(ngrams[n], start=1):
            print(f"Translating {n}-gram no. {enum} / {len(ngrams[n])}")
            target_ngram = str(
                translator.translate(source_ngram, "Swedish")
            ).lower()  # TODO: Target language should be variable-based
            source_target_pairs.append((source_ngram, target_ngram))

    create_csv_file(source_target_pairs)


def read_ngram_files(user_desired_ngrams=[2, 3, 4, 5, 6], data_size=500):
    """
    Reads N-gram files depending on which N-grams the user wants to output.

    Appends the N-grams to a dict with a size of data_size per N-gram (specified by user).
    """

    ngrams = {n: [] for n in user_desired_ngrams}

    for n in user_desired_ngrams:
        with open(f"./ngrams/{n}-grams.csv") as ngram_file:
            read_csv = csv.reader(ngram_file)
            for enum, row in enumerate(read_csv):
                if enum == data_size:
                    break
                ngrams[n].append(row[0])

    machine_translate_ngrams(ngrams)


# CODE TESTING:

read_ngram_files()
