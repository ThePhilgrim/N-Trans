from nltk import ngrams
import re
import collections


# String for testing
test_string = """
This is a sentence that will appear one time. Now this would be a sentence that appears 0 times. That's because there is a number in it. The number was a 0. Okay, this is a sentence that will appear twice. Okay, this is a sentence that will appear twice. I will also include a sentence that appear like ten times. This is it! This is it! This is it! This is it! This is it! This is it! This is it! This is it! This is it! This is it! Now the question is if this is enough. Maybe I should add a sentence that shows up a few more times? No, that's it. I'm done. I'm tired of coming up with new sentences that don't make any sense. That's it.. I'm done. Good bye! See ya later alligator. In a while, crocodile.
"""


def count_ngram_frequency(gram_list, x_most_common_grams):
    return collections.Counter(gram_list).most_common(x_most_common_grams)


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
    tuple_list = []

    for gram in x_grams:
        tuple_list.append(gram)

    # Joins tuples into strings, and deletes strings with numbers.
    gram_list = []

    for tuple in tuple_list:
        joined_tuple = ' '.join(tuple)
        if not any(char.isdigit() for char in joined_tuple):
            gram_list.append(joined_tuple)

    return count_ngram_frequency(gram_list, x_most_common_grams)


"""
CODE TESTING:
"""

# x_gram_length = int(input("How many words do you want to split your N-grams into? (int): "))

# list_length = int(input("How many of the most common N-grams do you want to produce? (int): "))

print(create_ngram(test_string, 6, 100))
