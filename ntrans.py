import nltk
import translatepy
import re
import collections
import csv
# import ssl


def prepare_corpus_data(data_size=1000000):
    # TODO: Put code that downloads BNC here

    bnc_corpus = nltk.corpus.BNCCorpusReader(root='BNC/Texts/', fileids=r'[A-K]/\w*/\w*\.xml')

    bnc_sents = []

    # TODO:
    # If user wants a smaller data set than the full corpus, it would be better
    # to pick random sents() from bnc_corpus instead of for looping over the first
    # X sents. If data_size = 10.000, pick 10.000 random sents from bnc_corpus

    for count, sentence in enumerate(bnc_corpus.sents()):
        string_sent = ' '.join(sentence)
        bnc_sents.append(string_sent)
        if count == 1000000:  # TODO: Change count == 10000 to "count == data_size"
            print(count)
            break
        # TODO: Remake print(count) to progress bar in tkinter
        if count % 1000 == 0:
            print(count)

    return ' '.join(bnc_sents)

    ### Outdated code. Will be deleted when BNC surely works as data source.
    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     pass
    # else:
    #     ssl._create_default_https_context = _create_unverified_https_context
    #
    # # Find what corpora are most suited for N-Trans
    # nltk.download('brown')
    # nltk.download('abc')
    # nltk.download('dependency_treebank')
    # # nltk.download('movie_reviews')
    #
    # # temporary variables for testing different corpora
    # brown_data = ' '.join(nltk.corpus.brown.words())
    # abc_data = ' '.join(nltk.corpus.abc.words())
    # dependency_treebank_data = ' '.join(nltk.corpus.dependency_treebank.words())  # Bad for 5-grams
    # movie_data = ' '.join(nltk.corpus.movie_reviews.words())
    # return abc_data
    # # return dependency_treebank_data + ' ' + abc_data + ' ' + brown_data + ' ' + movie_data


def create_csv_file(source_target_pairs, save_path=None):
    path = "/Users/Writing/Desktop/"  # TODO: Make path depend on user input and use "save_path"
    filename = "ntrans-glossary.csv"  # TODO: Make filename depend on user input
    full_path = path + filename

    with open(full_path, mode='w') as write_ntrans_file:
        data_writer = csv.writer(write_ntrans_file, delimiter=',')

        data_writer.writerow(('English', 'Swedish'))
        for source_target_pair in source_target_pairs:
            data_writer.writerow(source_target_pair)

    return print("N-Trans CSV Glossary has been successfully saved to " + full_path)


def machine_translate_ngrams(list_of_ngrams, language=None):

    translator = translatepy.Translator()

    source_target_pairs = []

    for enum_count, source_string in enumerate(list_of_ngrams, start=1):
        print(f"Translating item {enum_count}/{len(list_of_ngrams)}")
        translated_string = translator.translate(
            source_string, "Swedish"
        )  # TODO: Change to language variable
        # print(source_string + " --> " + str(translated_string))
        source_target_pairs.append((source_string, str(translated_string).lower()))

    create_csv_file(source_target_pairs)


def count_ngram_frequency(ngram_strings, desired_data_size):
    print('Counting N-gram frequency')
    x_most_common_ngrams = collections.Counter(ngram_strings).most_common(desired_data_size)
    print(x_most_common_ngrams)
    # return [ngram[0] for ngram in x_most_common_ngrams]


def create_ngrams(corpus_data, ngram_size, desired_data_size):
    """
    Strips string from special characters, creates tuple n_grams, deletes tuples
    with numbers, joins tuples into strings
    """

    # Removes punctuation and special characters from string.
    print('Removing punctuation...')
    text_without_punctuation = re.sub(r"[^\w']+", " ", corpus_data).lower()
    print('Fixing apostrophies...')

    # TODO: Make the .replaces more effective
    text_without_punctuation = text_without_punctuation.replace(" '", "'")
    text_without_punctuation = text_without_punctuation.replace(" n't", "n't")

    # TODO: Put ngram function in for loop to include all N-grams that the user wants.
    # TODO: Switch place of ngram creation and joining ngram_tuples into strings, since joining ngram_tuples takes a long time.
    # Splits string into N-grams and adds them to tuple_list.
    print('Creating N-grams')
    generated_ngram_tuples = nltk.ngrams(text_without_punctuation.split(), ngram_size)

    # Joins tuples into strings, and deletes strings with numbers.
    # TODO: Takes long time. Possible to make faster?
    ngram_strings = []
    print('Joining n-gram tuples to strings')
    for generated_ngram_tuple in generated_ngram_tuples:
        joined_tuple = " ".join(generated_ngram_tuple)
        if not any(char.isdigit() for char in joined_tuple):
            ngram_strings.append(joined_tuple)

    count_ngram_frequency(ngram_strings, desired_data_size)
    # # return machine_translate_ngrams(count_ngram_frequency(ngram_strings, desired_data_size))


"""
CODE TESTING:
"""

# ngram_size = int(input("How many words do you want to split your N-grams into? (int): "))

# desired_data_size = int(input("How many of the most common N-grams do you want to produce? (int): "))


corpus_data = prepare_corpus_data()
create_ngrams(corpus_data, 2, 100)
