import webbrowser
import tkinter
import functools
from tkinter import (
    filedialog,
)  # TODO: Figure out why I can't remove this import and use tkinter.filedialog... "self.savepath = tkinter.filedialog.askdirectory()" gives AttributeError: module 'tkinter' has no attribute 'filedialog'
from tkinter import ttk


class NTransMainGui:
    """
    Constitutes the main settings window where the user customize their N-Trans dictionary
    """

    def __init__(self) -> None:
        # Window & Frame
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("N-Trans")

        mainframe = ttk.Frame(self.root)
        mainframe.pack(fill="both", expand=True)

        header = ttk.Label(
            mainframe,
            text="N-Trans Dictionary Settings",
            font=("TkDefaultFont", 18),
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
        generate_button_style = ttk.Style()
        generate_button_style.configure(
            "W.TButton",
            font=("TkDefaultFont", 16),
            foreground="yellow",
            background="black",
            padding=30,
        )
        generate_dictionary = ttk.Button(
            mainframe,
            command=self.generate_ntrans_dictionary,
            text="Generate N-Trans Dictionary",
            style="W.TButton",
        )

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

        # Black turn off formatting
        # fmt: off

        # ==================
        # Widget placement
        # ==================
        header.grid(column=0, row=0, columnspan=2, padx=(0, 0), pady=(30, 30))

        ngram_check_label.grid(sticky="N", column=0, row=1, padx=(20, 0), pady=(10, 10))

        select_all_checkbutton.grid(sticky="W", column=0, row=2, padx=(40, 0), pady=(0, 10))

        for n in n_to_ngram_checkbox:
            n_to_ngram_checkbox[n].grid(sticky="W", column=0, padx=(40, 0), pady=(0, 0))

        data_size_label.grid(sticky="W", column=0, row=8, padx=(20, 0), pady=(30, 0))
        ngram_data_size.grid(sticky="W", column=0, row=9, padx=(20, 0), pady=(5, 0))

        target_language_label.grid(sticky="W", column=0, row=10, padx=(20, 20), pady=(30, 0))
        target_language.grid(sticky="W", column=0, row=11, padx=(20, 20), pady=(0, 0))

        filepath_label.grid(sticky="W", column=0, row=12, padx=(20, 0), pady=(30, 10))
        show_filepath.grid(sticky="W", column=0, row=13, padx=(20, 0), pady=(0, 10))
        get_savepath_button.grid(sticky="W", column=1, row=13, padx=(0, 20), pady=(0, 10))

        generate_dictionary.grid(column=0, row=14, columnspan=2, padx=(0, 0), pady=(30, 30))

        about_help_buttonframe.grid(sticky="E", column=0, row=15, columnspan=2, padx=(20, 20), pady=(0, 10))
        about_button.pack(side="left")
        help_button.pack(side="right")

        # Black turn on formatting
        # fmt: on

    def get_save_file_path(self) -> None:
        self.savepath: str = filedialog.askdirectory()  # type: ignore
        if self.savepath:
            self.filepath.set(self.savepath)
        print(type(self.savepath))

    def generate_ntrans_dictionary(self) -> None:
        self.user_choices = {
            "save_path": self.filepath.get(),
            "included_ngrams": [
                n for n, var in self.checkbox_vars.items() if var.get()
            ],
            "amount_of_ngrams": self.data_size_var.get(),
            "target_language": self.target_language_var.get(),
        }

        for key in self.user_choices:
            if not self.user_choices[key]:
                print(
                    "All fields need to be filled in before generating the N-Trans dictionary."
                )  # TODO: Change print to label
                break

        # TODO: Check filepath for validity

        # TODO: Call logic Here

    def open_help_page(self) -> None:
        webbrowser.open_new_tab(
            "https://www.google.com"
        )  # TODO: Write help document and link to it

    def select_all_ngrams(self) -> None:
        if self.select_all_var.get():
            for n in self.checkbox_vars:
                self.checkbox_vars[n].set(True)
        else:
            for n in self.checkbox_vars:
                self.checkbox_vars[n].set(False)

    def open_about_window(self) -> None:
        self.about_window = AboutWindow()

    def control_path_validity(self) -> None:
        pass

    def update_ngram_checkbox(self, n: int) -> None:
        if self.checkbox_vars[n].get():
            self.checkbox_vars[n].set(True)
        else:
            self.checkbox_vars[n].set(False)
            self.select_all_var.set(False)


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

        header.grid(column=0, row=0, padx=(0, 0), pady=(20, 20))
        main_text.grid(sticky="W", column=0, row=1, padx=(10, 30), pady=(0, 30))
        credit_text.grid(sticky="E", column=0, row=2, padx=(0, 30), pady=(30, 10))


ntrans_gui = NTransMainGui()
ntrans_gui.root.mainloop()
