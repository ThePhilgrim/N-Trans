import csv
import collections
import re
import nltk
import pathlib

"""
DEVELOPER INFO:

This script requires BNC (British National Corpus) to be downloaded to the local
system.

The full version of BNC can be downloaded from the Oxford Text Archive (538.35 MB):
http://www.ota.ox.ac.uk/desc/2554

Unzip BNC to the working directory, and rename the folder `BNC`.

"""


def write_data_to_csv(n_to_ngrams):
    """
    Writes the N-grams to CSV files. These CSV files are read from ntrans.py
    """

    filenames = ["2-grams", "3-grams", "4-grams", "5-grams", "6-grams"]
    pathlib.Path("ngrams").mkdir(exist_ok=True)

    for n, counter in n_to_ngrams.items():

        # "n - 2" to get index of "filenames"
        file_path = f"./ngrams/{n}-grams.csv"

        with open(file_path, mode="w") as write_data_file:
            data_writer = csv.writer(write_data_file, delimiter=",")

            for ngram, count in counter.most_common():
                csv_row = [" ".join(ngram), str(count)]
                data_writer.writerow(csv_row)


def count_ngram_frequency(n_to_ngrams):
    """
    Counts the frequency of each N-gram to distinguish the most common ones.
    """

    for n in n_to_ngrams.keys():
        n_to_ngrams[n] = collections.Counter(n_to_ngrams[n])

    # print(n_to_ngrams[2])
    write_data_to_csv(n_to_ngrams)


def generate_ngrams():
    """
    Extracts all sentences from the BNC in their raw format.
    Any sentence containing a number will be ignored.

    The remaining sencentes are processed by removing all punctuation &
    re-formatting contracted words, such as "can't" or "shouldn't".

    The sentences are then split into N-grams and added to lists,
    depending on the N-gram length.
    """

    n_to_ngrams = {
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    # Extracts <class 'nltk.corpus.reader.bnc.BNCSentence'> from BNC
    bnc_corpus = nltk.corpus.BNCCorpusReader(
        root="BNC/Texts/", fileids=r"[A-K]/\w*/\w*\.xml"
    )

    for count, sentence in enumerate(bnc_corpus.sents()[:100]):

        # Ignores any sentence that contains numbers
        if any(char.isdigit() for word in sentence for char in word):
            continue

        # Removes spaces in contracted words. Contracted words in
        # <class 'nltk.corpus.reader.bnc.BNCSentence'> are formatted "it 's" and "ca n't"
        contraction_index = [
            index for index, word in enumerate(sentence) if "'" in word
        ]
        for index in reversed(contraction_index):
            sentence[index - 1] += sentence.pop(index)

        # Removes all punctuation except apostrophies
        processed_sentence = [re.sub(r"[^\w']+", "", word.lower()) for word in sentence]

        # Removes empty strings left from removed punctuation
        processed_sentence = list(filter(None, processed_sentence))

        # Determines sentence length for deciding what N-grams to create from the current sentence
        sentence_length = len(processed_sentence)

        # Splits each sentence into N-grams and adds them to respective value in n_to_ngrams
        for n in n_to_ngrams.keys():
            if sentence_length >= n:
                n_to_ngrams[n].extend(nltk.ngrams(processed_sentence, n))

    count_ngram_frequency(n_to_ngrams)


generate_ngrams()
