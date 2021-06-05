import webbrowser
import tkinter
import tkinter.filedialog
import functools
import ntrans
import threading
import queue
import time
from tkinter import ttk
from typing import Optional


class NTransMainGui:
    """
    Constitutes the main settings window where the user customize their N-Trans dictionary
    """

    def __init__(self) -> None:
        self.thread: Optional[threading.Thread] = None
        self.cancel_thread_event = threading.Event()
        # Window & Frame
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("N-Trans")

        mainframe = ttk.Frame(self.root)
        mainframe.pack(fill="both", expand=True)

        header = ttk.Label(
            mainframe, text="N-Trans Dictionary Settings", font=("TkDefaultFont", 18)
        )

        # Get directory path to save csv file
        # TODO: Add default save path depending on OS
        get_savepath_button = ttk.Button(
            mainframe, command=self.get_save_file_path, text="Browse..."
        )

        self.filepath = tkinter.StringVar()

        filepath_label = ttk.Label(mainframe, text="Save N-Trans dictionary to")

        show_filepath = ttk.Entry(mainframe, textvariable=self.filepath, width=25)

        # What N-Grams to include in csv file.
        ngram_check_label = ttk.Label(mainframe, text="Choose N-grams to include")

        self.select_all_var = tkinter.BooleanVar(value=True)

        self.checkbox_vars = {n: tkinter.BooleanVar(value=True) for n in range(2, 7)}

        select_all_checkbutton = ttk.Checkbutton(
            mainframe,
            text="Select/Deselect all",
            variable=self.select_all_var,
            command=self.select_all_ngrams,
        )

        n_to_ngram_checkbox = {
            n: ttk.Checkbutton(
                mainframe,
                text=f"{n}-grams",
                variable=var,
                command=functools.partial(self.update_ngram_checkbox, n),
            )
            for n, var in self.checkbox_vars.items()
        }

        # What language to translate into
        target_language_label = ttk.Label(mainframe, text="Target language")

        self.target_language_var = tkinter.StringVar()

        target_language = ttk.Combobox(
            mainframe, state="readonly", textvariable=self.target_language_var
        )

        target_language["values"] = (
            "German",
            "Spanish",
            "French",
            "Swedish",
            "Italian",
        )

        # How many of each N-Gram to translate
        data_size_label = ttk.Label(mainframe, text="Amount of each N-gram to include")

        self.data_size_var = tkinter.IntVar()

        ngram_data_size = ttk.Combobox(
            mainframe, state="readonly", textvariable=self.data_size_var
        )

        ngram_data_size["values"] = (
            50,
            100,
            300,
            500,
            800,
            1000,
            1500,
            3000,
            5000,
            10000,
        )

        ngram_data_size.current(6)

        # Generate Button
        self.style_options = ttk.Style()
        self.style_options.configure(
            "W.TButton", font=("TkDefaultFont", 16), foreground="yellow", padding=30
        )

        self.style_options.configure("W.TLabel", foreground="red")

        generate_dictionary = ttk.Button(
            mainframe,
            command=self.generate_ntrans_dictionary,
            text="Generate N-Trans Dictionary",
            style="W.TButton",
        )

        # Warning for not all settings defined
        self.setting_not_defined_warning = ttk.Label(
            mainframe,
            text="All fields need to be filled in to start.",
            style="W.TLabel",
        )
        # Estimated Time
        self.estimated_time_label = ttk.Label(mainframe)
        self.update_estimated_time_label()

        # Progress Indication
        self.progress_frame = ttk.Frame(mainframe)
        self.progress_indicator = ProgressIndicator(self.progress_frame)

        self.cancel_button = ttk.Button(
            self.progress_frame, text="Cancel", command=self.cancel_generation
        )
        self.cancel_button.grid(column=0, row=1, columnspan=2, padx=(0, 0), pady=(0, 0))

        # About / Help
        about_help_buttonframe = ttk.Frame(mainframe)

        about_button = ttk.Button(
            about_help_buttonframe,
            command=self.open_about_window,
            text="About",
            style="",
        )  # TODO: Make command into lambda instantiating about-class
        help_button = ttk.Button(
            about_help_buttonframe, command=self.open_help_page, text="Help"
        )

        about_button.pack(side="left")
        help_button.pack(side="right")

        # Black turn off formatting
        # fmt: off

        # ==================
        # Widget placement
        # ==================
        header.grid(column=0, columnspan=2, padx=(0, 0), pady=(30, 30))

        ngram_check_label.grid(sticky="N", column=0, padx=(0, 0), pady=(10, 10))

        select_all_checkbutton.grid(sticky="W", column=0, padx=(40, 0), pady=(0, 10))

        for checkbox in n_to_ngram_checkbox.values():
            checkbox.grid(sticky="W", column=0, padx=(40, 0), pady=(0, 0))

        data_size_label.grid(sticky="W", column=0, padx=(20, 0), pady=(30, 0))
        ngram_data_size.grid(sticky="W", column=0, padx=(20, 0), pady=(5, 0))

        target_language_label.grid(sticky="W", column=0, padx=(20, 20), pady=(30, 0))
        target_language.grid(sticky="W", column=0, padx=(20, 20), pady=(0, 0))

        filepath_label.grid(sticky="W", column=0, padx=(20, 0), pady=(30, 10))
        show_filepath.grid(sticky="W", column=0, padx=(20, 0), pady=(0, 0))
        get_savepath_button.grid(sticky="W", column=1, row=13, padx=(0, 20), pady=(0, 0))

        generate_dictionary.grid(column=0, columnspan=2, padx=(0, 0), pady=(0, 0))
        self.setting_not_defined_warning.grid(column=0, row=15, columnspan=2, padx=(0, 0), pady=(0, 0))
        self.estimated_time_label.grid(sticky="W", column=0, columnspan=2, padx=(30, 0), pady=(0, 0))

        about_help_buttonframe.grid(sticky="E", column=0, row=17, columnspan=2, padx=(20, 20), pady=(20, 10))

        # Black turn on formatting
        # fmt: on

        self.filepath.trace_add("write", self.update_user_choice_vars)
        self.target_language_var.trace_add("write", self.update_user_choice_vars)
        for var in self.checkbox_vars.values():
            var.trace_add("write", self.update_user_choice_vars)
            var.trace_add("write", self.update_estimated_time_label)

        self.data_size_var.trace_add("write", self.update_user_choice_vars)

        self.select_all_var.trace_add("write", self.update_estimated_time_label)
        self.data_size_var.trace_add("write", self.update_estimated_time_label)

        self.update_estimated_time_label()

    def flash_warning_label(self) -> None:
        for flash in range(3):
            self.style_options.configure("W.TLabel", foreground="orange")
            self.root.update()  # type: ignore
            time.sleep(0.07)
            self.style_options.configure("W.TLabel", foreground="red")
            self.root.update()  # type: ignore
            time.sleep(0.07)
        # self.style_options.configure("W.TLabel", foreground="red")

    def update_user_choice_vars(self, *junk: object) -> None:
        if (
            self.filepath.get()
            and self.target_language_var.get()
            and any(var.get() for var in self.checkbox_vars.values())
        ):
            self.setting_not_defined_warning.grid_remove()
        else:
            self.setting_not_defined_warning.grid()

    def get_save_file_path(self) -> None:
        savepath = tkinter.filedialog.askdirectory()  # type: ignore
        if savepath:
            self.filepath.set(savepath)

    def generate_ntrans_dictionary(self) -> None:
        user_choices = {
            "save_path": self.filepath.get(),
            "included_ngrams": [
                n for n, var in self.checkbox_vars.items() if var.get()
            ],
            "amount_of_ngrams": self.data_size_var.get(),
            "target_language": self.target_language_var.get(),
        }

        for key in user_choices:
            if not user_choices[key]:
                self.flash_warning_label()
                return

        self.cancel_thread_event.clear()

        # TODO: Check filepath for validity
        if self.thread is None:
            self.progress_queue: queue.Queue[int] = queue.Queue()
            # Calls logic in ntrans.py
            self.thread = threading.Thread(
                target=ntrans.read_ngram_files,
                args=[user_choices, self.progress_queue, self.cancel_thread_event],
            )
            self.thread.start()

            self.estimated_time_label.grid_remove()
            self.progress_frame.grid(
                column=0, row=16, columnspan=2, padx=(0, 0), pady=(20, 40)
            )
            self.check_progressbar_queue()

    def check_progressbar_queue(self) -> None:
        try:
            current_percentage = self.progress_queue.get(block=False)
            self.progress_indicator.update_progress_value(current_percentage)
        except queue.Empty:
            pass

        if self.thread is not None:
            self.root.after(100, self.check_progressbar_queue)
        else:
            self.progress_frame.grid_remove()

    def select_all_ngrams(self) -> None:
        for var in self.checkbox_vars.values():
            var.set(self.select_all_var.get())

    def open_about_window(self) -> None:
        self.about_window = AboutWindow()

    def open_help_page(self) -> None:
        webbrowser.open_new_tab(
            "https://www.google.com"
        )  # TODO: Write help document and link to it

    def control_path_validity(
        self,
    ) -> None:  # TODO: Add logic to make sure the save path is a valid path.
        pass

    def update_ngram_checkbox(self, n: int) -> None:
        self.checkbox_vars[n].get()

        if not self.checkbox_vars[n].get():
            self.select_all_var.set(False)

    # *junk is random tcl stuff that trace_add wants in the callback method.
    def update_estimated_time_label(self, *junk: object) -> None:
        total_time_in_seconds = int(
            self.data_size_var.get()
            * len([n for n, var in self.checkbox_vars.items() if var.get()])
            * 1.2
        )  # Average time in seconds per N-gram
        if total_time_in_seconds >= 60 * 60:
            self.estimated_time_label[
                "text"
            ] = f"Estimated run time: {int(total_time_in_seconds / 60 / 60)} h & {int(total_time_in_seconds / 60 % 60)} min"
        elif total_time_in_seconds >= 60:
            if total_time_in_seconds % 60 == 0:
                self.estimated_time_label[
                    "text"
                ] = f"Estimated run time: {int(total_time_in_seconds / 60)} min"
            else:
                self.estimated_time_label[
                    "text"
                ] = f"Estimated run time: {int(total_time_in_seconds / 60)} min & {total_time_in_seconds % 60} sec"
        else:
            self.estimated_time_label[
                "text"
            ] = f"Estimated run time: {total_time_in_seconds} sec"

    def cancel_generation(self) -> None:
        self.cancel_thread_event.set()
        self.thread = None


class ProgressIndicator:
    def __init__(self, parent_frame: ttk.Frame) -> None:
        self.progress_bar = ttk.Progressbar(
            parent_frame, length=250, orient="horizontal", mode="determinate"
        )

        self.percentage_label = ttk.Label(parent_frame)

        self.progress_bar.grid(column=0, row=0, padx=(0, 0), pady=(0, 0))
        self.percentage_label.grid(column=1, row=0, padx=(5, 0), pady=(0, 0))

    def update_progress_value(self, current_percentage: int) -> None:
        self.progress_bar["value"] = current_percentage
        self.percentage_label["text"] = str(current_percentage) + "%"


class AboutWindow:
    def __init__(self) -> None:
        self.about_window = tkinter.Toplevel()
        self.about_window.resizable(False, False)
        self.about_window.title("About N-Trans")

        mainframe = ttk.Frame(self.about_window)
        mainframe.pack(fill="both", expand=True)

        header = ttk.Label(mainframe, text="About N-Trans", font=("TkDefaultFont", 18))

        main_text = ttk.Label(
            mainframe,
            text="""
        N-Trans is written by Philip Sundt to help professional translators improve
        workflow in their CAT tool of choice.

        The generated N-Trans dictionary is based on the most frequent N-grams
        in the British National Corpus.

        Disclaimer: The N-Trans dictionary is machine translated and is meant
        to be used as a complement to manual human translations. Any incorrect
        or poor quality machine translations should be edited in the termbase.
        The quality of the translations in the N-Trans dictionary cannot be
        guaranteed. No developer of N-Trans can be held responsible for poor
        quality translations made as a direct or indirect result of the N-Trans
        dictionary.
        """,
        )  # TODO: Improve main text

        credit_text = ttk.Label(mainframe, text="Thanks to Akuli")

        header.grid(column=0, padx=(0, 0), pady=(20, 20))
        main_text.grid(sticky="W", column=0, padx=(10, 30), pady=(0, 30))
        credit_text.grid(sticky="E", column=0, padx=(0, 30), pady=(30, 10))


# TODO: Create progress bar window for when logic is called


ntrans_gui = NTransMainGui()
ntrans_gui.root.mainloop()
