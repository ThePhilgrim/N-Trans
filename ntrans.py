"""
The usage of this script relies on the N-gram files in "./ngrams"

These files are generated through ntrans_dataprep.py and processed in ntrans_combine.py
"""
from __future__ import annotations
import translatepy  # type: ignore
import csv
import queue
import threading
from typing import List, Dict, Tuple, Any


SourceTarget = Tuple[str, str]


class GlossaryGenerator:
    def __init__(
        self,
        user_choices: Dict[str, Any],
        progress_queue: queue.Queue[int],
        cancel_thread_event: threading.Event,
        generation_finished_event: threading.Event,
    ) -> None:
        self.user_choices = user_choices
        self.progress_queue = progress_queue
        self.cancel_thread = cancel_thread_event
        self.generation_finished_event = generation_finished_event

    def create_csv_file(self, source_target_pairs: List[SourceTarget]) -> None:
        """
        Writes source N-Gram and its translation to csv file.
        """
        save_path = self.user_choices["save_path"]

        filename = "ntrans-glossary.csv"  # TODO: Make filename depend on user input

        with open(f"{save_path}/{filename}", mode="w") as write_ntrans_file:
            data_writer = csv.writer(write_ntrans_file)

            data_writer.writerow(("English", self.user_choices["target_language"]))
            for source_target_pair in source_target_pairs:
                data_writer.writerow(source_target_pair)

        return

    def machine_translate_ngrams(self, ngrams: Dict[int, List[str]]) -> None:
        """
        Translates each N-gram and appends the source/target pair to a list.
        """
        source_target_pairs: List[SourceTarget] = []

        translator = translatepy.Translator()

        total_translations = (
            len(self.user_choices["included_ngrams"])
            * self.user_choices["amount_of_ngrams"]
        )

        for key, value in ngrams.items():
            for enum, source_ngram in enumerate(value, start=1):
                if self.cancel_thread.is_set():
                    return
                target_ngram = str(
                    translator.translate(
                        source_ngram, self.user_choices["target_language"]
                    )
                ).lower()
                source_target_pairs.append((source_ngram, target_ngram))
                self.progress_queue.put(
                    int(len(source_target_pairs) / total_translations * 100)
                )

        self.create_csv_file(source_target_pairs)

    def read_ngram_files(self) -> None:
        """
        Reads N-gram files depending on which N-grams the user wants in their N-Trans Dictionary.
        Appends the N-grams to a dict with a size of data_size per N-gram (specified by user).
        """

        ngrams: Dict[int, List[str]] = {
            n: [] for n in self.user_choices["included_ngrams"]
        }

        for n in ngrams:
            with open(f"./ngrams/{n}-grams.csv") as ngram_file:
                read_csv = csv.reader(ngram_file)
                for enum, row in enumerate(read_csv):
                    if enum == self.user_choices["amount_of_ngrams"]:
                        break
                    ngrams[n].append(row[0])

        self.machine_translate_ngrams(ngrams)
