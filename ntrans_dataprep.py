"""
This script requires BNC (British National Corpus) to be downloaded to the local
system.

The full version of BNC can be downloaded from the Oxford Text Archive (538.35 MB):
http://www.ota.ox.ac.uk/desc/2554

Unzip BNC to the working directory, and rename the folder `BNC`.

NOTE: The BNC contains around 112.000.000 words (or 5.397.000 sentences).
It can take around 2 hours to run this script.

"""

import csv
import collections
import re
import nltk
import pathlib


def write_data_to_csv(n_to_ngrams):
    """
    Writes the N-grams to CSV files. These CSV files are read from ntrans.py
    """

    pathlib.Path("ngrams").mkdir(exist_ok=True)

    for n, collections_counter in n_to_ngrams.items():
        file_path = f"./ngrams/{n}-grams.csv"

        with open(file_path, mode="w") as write_data_file:
            data_writer = csv.writer(write_data_file)

            for ngram, count in collections_counter.most_common():
                csv_row = [" ".join(ngram), str(count)]
                data_writer.writerow(csv_row)


def count_ngram_frequency(n_to_ngrams):
    """
    Counts the frequency of each N-gram to distinguish the most common ones.
    """

    # Example output: "2: Counter({('of', 'the'): 64, ('in', 'the'): 48, ('gift', 'aid'): 27..."
    write_data_to_csv(
        {n: collections.Counter(ngrams) for n, ngrams in n_to_ngrams.items()}
    )


def format_corpus_sents(sentence):
    """
    Reformats spaces in contracted words. Contracted words in
    <class 'nltk.corpus.reader.bnc.BNCSentence'> are formatted "it 's" and "ca n't"

    Removes all punctuation except apostrophies, and removes the empty strings left from the deleted
    apostrophies
    """

    contraction_index = [index for index, word in enumerate(sentence) if "'" in word]
    for index in reversed(contraction_index):
        if index != 0:
            sentence[index - 1] += sentence.pop(index)

    processed_sentence = [re.sub(r"[^\w']+", "", word.lower()) for word in sentence]

    return list(filter(None, processed_sentence))


def generate_ngrams_from_corpus():
    """
    Extracts all sentences from the BNC in their raw format.
    Any sentence containing a number will be ignored.

    The sentences are formatted in format_corpus_sents()

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

    # To work with a sample size of the BNC, add a range in sents().
    # For example "for count, sentence in enumerate(bnc_corpus.sents()[:1000]):"
    for count, sentence in enumerate(bnc_corpus.sents()):

        # Ignores any sentence that contains numbers
        if any(char.isdigit() for word in sentence for char in word):
            continue

        processed_sentence = format_corpus_sents(sentence)

        # Determines sentence length for deciding what N-grams to create from the current sentence
        sentence_length = len(processed_sentence)

        # Splits each sentence into N-grams and adds them to respective value in n_to_ngrams
        for n in n_to_ngrams.keys():
            if sentence_length >= n:
                n_to_ngrams[n].extend(nltk.ngrams(processed_sentence, n))

    count_ngram_frequency(n_to_ngrams)


generate_ngrams_from_corpus()
