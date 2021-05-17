import csv
import collections
import re
import nltk

"""
DEVELOPER INFO:

This script requires BNC (British National Corpus) to be downloaded to the local
system.

The full version of BNC can be downloaded from the Oxford Text Archive (538.35 MB):
http://www.ota.ox.ac.uk/desc/2554

Unzip BNC to the working directory, and rename the folder `BNC`.

"""


def write_data_to_csv(
    counted_two_grams,
    counted_three_grams,
    counted_four_grams,
    counted_five_grams,
    counted_six_grams,
):
    """
    Writes the N-grams to CSV files. These CSV files are read from ntrans.py
    """
    pass


def count_ngram_frequency(twograms, threegrams, fourgrams, fivegrams, sixgrams):
    """
    Counts the frequency of each N-gram to distinguish the most common ones.
    """
    counted_two_grams = collections.Counter(twograms)
    counted_three_grams = collections.Counter(threegrams)
    counted_four_grams = collections.Counter(fourgrams)
    counted_five_grams = collections.Counter(fivegrams)
    counted_six_grams = collections.Counter(sixgrams)

    write_data_to_csv(
        counted_two_grams,
        counted_three_grams,
        counted_four_grams,
        counted_five_grams,
        counted_six_grams,
    )


def generate_ngrams():
    """
    Extracts all sentences from the BNC in their raw format.
    Any sentence containing a number will be ignored.

    The remaining sencentes are processed by removing all punctuation &
    re-formatting contracted words, such as "can't" or "shouldn't".

    The sentences are then split into N-grams and added to lists,
    depending on the N-gram length.
    """

    two_grams = []
    three_grams = []
    four_grams = []
    five_grams = []
    six_grams = []

    # Extracts <class 'nltk.corpus.reader.bnc.BNCSentence'> from BNC
    bnc_corpus = nltk.corpus.BNCCorpusReader(
        root="BNC/Texts/", fileids=r"[A-K]/\w*/\w*\.xml"
    )

    for count, sentence in enumerate(bnc_corpus.sents()[:10000]):

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

        # Splits each sentence into N-grams and adds them to respective lists
        if sentence_length >= 6:
            six_grams.extend(nltk.ngrams(processed_sentence, 6))
        if sentence_length >= 5:
            five_grams.extend(nltk.ngrams(processed_sentence, 5))
        if sentence_length >= 4:
            four_grams.extend(nltk.ngrams(processed_sentence, 4))
        if sentence_length >= 3:
            three_grams.extend(nltk.ngrams(processed_sentence, 3))
        if sentence_length >= 2:
            two_grams.extend(nltk.ngrams(processed_sentence, 2))

    count_ngram_frequency(two_grams, three_grams, four_grams, five_grams, six_grams)


generate_ngrams()
