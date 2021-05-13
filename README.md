# N-Trans



## Introduction

N-Trans creates a database of the X most common N-grams (https://en.wikipedia.org/wiki/N-gram) in the English language from
the American Google Corpus (https://www.english-corpora.org/googlebooks/x.asp).

Thereafter, it uses Google Translate (https://translate.google.com/) to translate the N-grams into a chosen
target language, and creates a dictionary in CSV format.

The purpose of N-Trans is to aid translators by enhancing workflow in their CAT tool of choice.



## For Users

Thank you for your interest in using N-Trans.

Please note that N-Trans is still under development, and is not yet in a usable state.
A certain understanding of programming is required to use N-Trans at this stage.



## For Developers

It is recommended to work on N-Trans in a virtual environment.

To set up a virtual environment:
- MAC OS:
  `python3 -m venv env`

To activate a virtual environment:
- MAC OS:
  `source env/bin/activate`



### Libraries


#### NLTK (Docs: https://www.nltk.org/)

To install NLTK:
- MAC OS:
  `python3 -m pip install nltk`

NLTK is used to process the data and create N-grams from it.


#### Re (Docs: https://docs.python.org/3/library/re.html)

Re is used to remove punctuation & special characters from the downloaded data

#### collections.Counter (Docs: https://docs.python.org/3/library/collections.html)

collections.Counter is used to count the frequency of each N-gram to distinguish the most common ones.

#### translatepy (Docs: https://github.com/Animenosekai/translate)

To install translatepy:
- MAC OS:
  `python3 -m pip install translatepy`

Translatepy is used to, with the help of several machine translation APIs, translate the X most common N-grams.


#### CSV (Docs: https://docs.python.org/3/library/csv.html)

CSV is used to create the N-Trans glossary file.


### Tools


#### Black (Docs: https://pypi.org/project/black/)
This project uses Black to format the code. Please use Black before creating a PR.

To install Black:
- MAC OS:
  `python3 -m pip install black`

To use Black:
- MAC OS:
  `black ntrans.py`
