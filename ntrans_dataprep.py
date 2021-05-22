"""
This script requires BNC (British National Corpus) to be downloaded to the local
system.

The full version of BNC can be downloaded from the Oxford Text Archive (538.35 MB):
http://www.ota.ox.ac.uk/desc/2554

Unzip BNC to the working directory, and rename the folder `BNC`.

NOTE: The BNC contains around 112M words (or 6M+ sentences).
It can take around 1,5 hours to run this script.

The script generates 237M N-grams.

"""

from __future__ import annotations

import csv
import collections
import re
import nltk  # type: ignore
import pathlib
from datetime import datetime
from typing import List, Dict, Tuple


NGram = Tuple[str, ...]


def write_data_to_csv(
    n_to_ngrams: Dict[int, collections.Counter[NGram]], chunk_number: int
) -> None:
    """
    Writes the N-grams to CSV files in chunks of 300K sentences.

    """

    pathlib.Path("ngrams").mkdir(exist_ok=True)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print(
        "Writing data chunk #"
        + str(chunk_number)
        + " to csv – Current time: "
        + current_time
    )

    for n, collections_counter in n_to_ngrams.items():
        file_path = f"./ngrams/chunk{chunk_number}_{n}-grams.csv"

        with open(file_path, mode="w") as write_data_file:
            data_writer = csv.writer(write_data_file)

            for ngram, count in collections_counter.most_common():
                csv_row = [" ".join(ngram), str(count)]
                data_writer.writerow(csv_row)


def count_ngram_frequency(
    n_to_ngrams: Dict[int, List[NGram]]
) -> Dict[int, collections.Counter[NGram]]:
    """
    Counts the frequency of each N-gram to distinguish the most common ones.
    """

    # Example output: "2: Counter({('of', 'the'): 64, ('in', 'the'): 48, ('gift', 'aid'): 27..."
    return {n: collections.Counter(ngrams) for n, ngrams in n_to_ngrams.items()}


def format_corpus_sents(sentence: List[str]) -> List[str]:
    """
    Reformats spaces in contracted words. Contracted words in
    <class 'nltk.corpus.reader.bnc.BNCSentence'> are formatted "it 's" and "ca n't".

    Removes all punctuation except apostrophies, and removes the empty strings left from the deleted
    apostrophies.
    """

    sentence = sentence.copy()

    contraction_index = [index for index, word in enumerate(sentence) if "'" in word]
    for index in reversed(contraction_index):
        if index != 0:
            sentence[index - 1] += sentence.pop(index)

    processed_sentence = [re.sub(r"[^\w']+", "", word.lower()) for word in sentence]

    return list(filter(None, processed_sentence))


def generate_ngrams_from_corpus() -> None:
    """
    Extracts all sentences from the BNC in their raw format.
    Any sentence containing a number will be ignored.

    The sentences are formatted before they are split into N-grams and added to lists, depending on
    the N-gram length.
    """
    # TODO: Update Docstring to explain csv split process

    n_to_ngrams: Dict[int, List[NGram]] = {
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

    chunk_number = 1

    # To work with a sample size of the BNC, add a range in sents().
    # For example "for count, sentence in enumerate(bnc_corpus.sents()[:1000]):"
    for count, sentence in enumerate(bnc_corpus.sents()):
        if count % 10000 == 0:
            print(count)

        if count != 0 and count % 300000 == 0:
            write_data_to_csv(count_ngram_frequency(n_to_ngrams), chunk_number)
            chunk_number += 1

            # Avoids filling up RAM
            for n in n_to_ngrams:
                n_to_ngrams[n].clear()

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

    write_data_to_csv(count_ngram_frequency(n_to_ngrams), chunk_number)


generate_ngrams_from_corpus()
