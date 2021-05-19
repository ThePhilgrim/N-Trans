# import translatepy
# import csv

"""
DEVELOPER INFO:

The usage of this script relies on the N-gram files in "./ngrams"

These files are created through ntrans_dataprep.py
"""


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



"""
CODE TESTING:
"""
