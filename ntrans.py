from nltk import ngrams
from googletrans import Translator
import re
import collections


# String for testing
test_string = """
The bikers rode down the long and narrow path to reach the city park. When they reached a good spot to rest, they began to look for signs of spring. The sun was bright, and a lot of bright red and blue blooms proved to all that warm spring days were the very best. Spring rides were planned. They had a burger at the lake and then rode farther up the mountain. As one rider started to get off his bike, he slipped and fell. One of the other bikers saw him fall but could do nothing to help him. Neither the boy nor the bike got hurt. After a brief stop, everyone was ready to go on. All the bikers enjoyed the nice view when they came to the top. All the roads far below them looked like ribbons. A dozen or so boats could be seen on the lake. It was very quiet and peaceful and no one wished to leave. As they set out on their return, they all enjoyed the ease of pedaling. The bikers came upon a new bike trail. This route led to scenery far grander than that seen from the normal path. The end of the day brought laughs and cheers from everyone. The fact that each person was very, very tired did not keep anyone from eagerly planning for the exciting ride to come.
"""


def machine_translate_ngrams(prepared_ngram_list, language=None):
    translated_ngram_list = []

    translator = Translator()

    translated_ngrams = translator.translate(prepared_ngram_list, dest='sv')  # TODO: Change language to variable

    for translated_ngram in translated_ngrams:
        source_and_target = translated_ngram.origin[0], translated_ngram.text
        translated_ngram_list.append(source_and_target)

    return translated_ngram_list


def count_ngram_frequency(gram_list, x_most_common_grams):
    counted = collections.Counter(gram_list).most_common(x_most_common_grams)

    return [ngram[0] for ngram in counted]


def create_ngram(string, n_gram_length, x_most_common):
    '''
    Strips string from special characters, creates tuple n_grams, deletes tuples
    with numbers, joins tuples into strings
    '''

    # Determines the size of the returned dictionary from count_ngram_frequency()
    x_most_common_grams = x_most_common

    # Removes punctuation and special characters from string.
    clean_string = re.sub(r"[^\w']+", " ", string).lower()

    # Splits string into N-grams and adds them to tuple_list.
    x_grams = ngrams(clean_string.split(), n_gram_length)

    # Joins tuples into strings, and deletes strings with numbers.
    n_gram_list = []

    for tuple in x_grams:
        joined_tuple = ' '.join(tuple)
        if not any(char.isdigit() for char in joined_tuple):
            n_gram_list.append(joined_tuple)

    prepared_ngram_list = count_ngram_frequency(n_gram_list, x_most_common_grams)

    return machine_translate_ngrams(prepared_ngram_list)


"""
CODE TESTING:
"""

# x_gram_length = int(input("How many words do you want to split your N-grams into? (int): "))

# list_length = int(input("How many of the most common N-grams do you want to produce? (int): "))

create_ngram(test_string, 2, 3)

# print(create_ngram(test_string, 2, 10))
