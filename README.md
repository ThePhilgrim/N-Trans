# N-Trans

## Introduction

N-Trans creates a database of the X most common N-grams in the English language from
the Google Corpus (LINK HERE).

Thereafter, it uses Google Translate (LINK HERE) to translate the N-grams into a chosen
target language, and creates a dictionary in CSV format.

The purpose of N-Trans is to aid translators by enhancing workflow in their CAT tool of choice.

## For Users
-

## For Developers
It is recommended to work on N-Trans in a virtual environment.

To set up a virtual environment:
- MAC OS:
  `python3 -m venv env`

To activate a virtual environment:
- MAC OS:
  `source env/bin/activate`

### Libraries

#### NLTK

#### googletrans


### Tools

#### Black
This project uses Black to format the code. Please use Black before creating a PR.

To install Black:
- MAC OS:
  `python3 -m pip install black`

To use Black:
- MAC OS:
  `black ntrans.py`
