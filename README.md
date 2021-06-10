# N-Trans



## Introduction

N-Trans creates a database of the X most common N-grams (https://en.wikipedia.org/wiki/N-gram) in the English language from
the British National Corpus (https://www.english-corpora.org/bnc/).

Thereafter, it uses various machine translation providers (read more: https://pypi.org/project/translatepy/) to translate the N-grams into a chosen
target language, and creates a dictionary in CSV format.

The purpose of N-Trans is to aid translators by enhancing workflow in their CAT tool of choice.



## For Users

Thank you for your interest in using N-Trans.

Please note that N-Trans is still under development, and is not yet in a usable state.
A certain understanding of programming is required to use N-Trans at this stage.

Please return to this page regularly to stay updated with the progress of development.


## For Developers

N-Trans is split into three phases.

1) In `ntrans_dataprep.py`, sentences from the BNC are processed and, split into N-grams, and written
to .csv files in chunks of 300K sentences. (In total, 105 .csv files are created).

2) In `ntrans_combine.py`, the frequency of each N-gram is counted with `collections.Counter`. The 10K
most frequent N-grams are thereafter written to a new .csv file. One file is created for each N-gram
(2-grams, 3-grams, etc.)

3) `ntrans.py` is the main program which the end user is exposed to. Here, the X most frequent N-grams
will be machine translated to a chosen target language, and the source-target pair is written to a .csv file.

### GUI & Data

#### GUI
The N-Trans GUI is written in tkinter, in combination with ttk.
Sadly, this results in significant GUI inconsistencies across systems. The GUI was written on
and has been optimized for Mac OS.

If you are on Linux or Windows, you are more than welcome to contribute to the GUI optimization of
these systems.


#### Data
The data is collected from the BNC with the help of the NLTK library. The hope is that more corpora
will be implemented in the future. Both to diversify the source data, and also to support more source languages.

The target languages are a selection from the available languages of the translatepy library.
The full list of available languages can be found in the translatepy repository.

N-Trans imports its supported target languages from `target_languages.json`.

### Development

It is recommended to work on N-Trans in a virtual environment.

To set up a virtual environment:
- MAC OS:
  `python3 -m venv env`
- Windows
  `py -m venv env`

To activate a virtual environment:
- MAC OS:
  `source env/bin/activate`
- Windows:
  `env\Scripts\activate`

#### Install Dependencies

To install the dependencies needed to develop & test N-Trans, run inside the virtualenv:

- MAC OS:
  `python3 -m pip install -r requirements.txt`
- Windows:
  `py -m pip install -r requirements.txt`

#### Formatting

This project uses Black to format the code. Please use Black before creating a PR.

To use Black:
`black file.py`
