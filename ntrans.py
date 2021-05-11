# from collections import Counter for counting instances of phrase
# Need to remove commas, full stops etc.

# To get rid of punctuation:
# https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer

from nltk import ngrams

# For testing N-gram creation
test_sentence = "The quick brown fox jumps over the lazy dog."

# For testing N-gram counting
test_double_sentence = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."

# For testing on larger text
test_paragraph = """
December 17, 1903, is the birth date of all airplanes.
Orville and Wilbur Wright started building gliders in 1900. In 1903, they built
a motor and propeller for their glider. Orville made the first flight, which
lasted 12 seconds, and flew 120 feet. Wilbur's flight was 852 feet in 59 seconds.
These first flights in 1903 were just the start of the evolution of planes.
By the year 1909, Bleriot had crossed the English Channel. By the year 1912,
a two-piece plywood fuselage was built for greater strength. By the 1930s,
the all-metal fuselage was tried, and it soon appeared in DC3s. From the Wrights'
1903 motor and prop came the engines for the 1950 turbojet that generated at least
19,600 pounds of thrust. The big Boeing 747 has four engines with 50,000 pounds
of thrust each. The future holds an advanced super-sonic jet with a saving of
almost 40 percent in fuel usage.
"""

n_2 = 2
n_3 = 3
n_4 = 4
n_5 = 5
n_6 = 6

fourgrams = ngrams(test_double_sentence.split(), n_4)

for grams in fourgrams:
    print(grams)
