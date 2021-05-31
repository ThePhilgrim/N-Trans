import tkinter
from tkinter import filedialog
from tkinter import ttk


class NTransMainGui:
    def __init__(self):
        # Window & Frame
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("N-Trans")

        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        # Header
        header = ttk.Label(
            self.mainframe,
            text="N-Trans Dictionary Settings",
            font=("TkDefaultFont", 18),
        )

        # Get directory path to save csv file
        get_savepath_button = ttk.Button(
            self.mainframe, command=self.get_save_file_path, text="Browse..."
        )

        self.filepath = tkinter.StringVar()

        filepath_label = ttk.Label(self.mainframe, text="Save N-Trans dictionary to")

        show_filepath = ttk.Entry(self.mainframe, textvariable=self.filepath, width=25)

        # What N-Grams to include in csv file.
        ngram_check_label = ttk.Label(self.mainframe, text="Choose N-grams to include")

        self.deselected = 0
        self.selected = 1

        self.select_all_checked = tkinter.IntVar(value=self.selected)
        self.two_gram_checked = tkinter.IntVar(value=self.selected)
        self.three_gram_checked = tkinter.IntVar(value=self.selected)
        self.four_gram_checked = tkinter.IntVar(value=self.selected)
        self.five_gram_checked = tkinter.IntVar(value=self.selected)
        self.six_gram_checked = tkinter.IntVar(value=self.selected)

        select_all_check = ttk.Checkbutton(
            self.mainframe,
            text="Select all",
            variable=self.select_all_checked,
            command=self.select_all_ngrams,
        )  # TODO: Add method that selects/deselects all and changes the text to reflect state.

        two_gram_check = ttk.Checkbutton(
            self.mainframe, text="2-grams", variable=self.two_gram_checked
        )

        three_gram_check = ttk.Checkbutton(
            self.mainframe, text="3-grams", variable=self.three_gram_checked
        )

        four_gram_check = ttk.Checkbutton(
            self.mainframe, text="4-grams", variable=self.four_gram_checked
        )

        five_gram_check = ttk.Checkbutton(
            self.mainframe, text="5-grams", variable=self.five_gram_checked
        )

        six_gram_check = ttk.Checkbutton(
            self.mainframe, text="6-grams", variable=self.six_gram_checked
        )

        # What language to translate into
        target_language_label = ttk.Label(self.mainframe, text="Target language")

        target_language_var = tkinter.StringVar()

        target_language = ttk.Combobox(
            self.mainframe, state="readonly", textvariable=target_language_var
        )

        target_language["values"] = (
            "German",
            "Spanish",
            "French",
            "Swedish",
            "Italian",
        )

        target_language.current()

        # How many of each N-Gram to translate
        data_size_label = ttk.Label(
            self.mainframe, text="Amount of each N-gram to include"
        )

        data_size_var = tkinter.StringVar()

        ngram_data_size = ttk.Combobox(
            self.mainframe, state="readonly", textvariable=data_size_var
        )

        ngram_data_size["values"] = (
            "100",
            "300",
            "500",
            "800",
            "1000",
            "1500",
            "3000",
            "5000",
            "10000",
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
        )  # TODO: Background not working
        generate_dictionary = ttk.Button(
            self.mainframe,
            command=self.generate_ntrans_dictionary,
            text="Generate N-Trans Dictionary",
            style="W.TButton",
        )

        # About / Help

        # To fit About & Help button in same column
        self.button_frame = ttk.Frame(self.mainframe)

        about_button = ttk.Button(
            self.button_frame, command=self.open_about_window, text="About", style=""
        )  # TODO: Make command into lambda instantiating about-class
        help_button = ttk.Button(
            self.button_frame, command=self.open_help_page, text="Help"
        )

        # Widget Positioning
        header.grid(column=0, row=0, columnspan=2, padx=(0, 0), pady=(30, 30))

        ngram_check_label.grid(sticky="N", column=0, row=1, padx=(20, 0), pady=(10, 10))

        select_all_check.grid(sticky="W", column=0, row=2, padx=(40, 0), pady=(0, 10))
        two_gram_check.grid(sticky="W", column=0, row=3, padx=(40, 0), pady=(0, 0))
        three_gram_check.grid(sticky="W", column=0, row=4, padx=(40, 0), pady=(0, 0))
        four_gram_check.grid(sticky="W", column=0, row=5, padx=(40, 0), pady=(0, 0))
        five_gram_check.grid(sticky="W", column=0, row=6, padx=(40, 0), pady=(0, 0))
        six_gram_check.grid(sticky="W", column=0, row=7, padx=(40, 0), pady=(0, 0))

        data_size_label.grid(sticky="W", column=0, row=8, padx=(20, 0), pady=(30, 0))
        ngram_data_size.grid(sticky="W", column=0, row=9, padx=(20, 0), pady=(5, 0))

        target_language_label.grid(
            sticky="W", column=0, row=10, padx=(20, 20), pady=(30, 0)
        )
        target_language.grid(sticky="W", column=0, row=11, padx=(20, 20), pady=(0, 0))

        filepath_label.grid(sticky="W", column=0, row=12, padx=(20, 0), pady=(30, 10))
        show_filepath.grid(sticky="W", column=0, row=13, padx=(20, 0), pady=(0, 10))
        get_savepath_button.grid(
            sticky="W", column=1, row=13, padx=(0, 20), pady=(0, 10)
        )

        generate_dictionary.grid(
            column=0, row=14, columnspan=2, padx=(0, 0), pady=(30, 30)
        )

        self.button_frame.grid(
            sticky="E", column=0, row=15, columnspan=2, padx=(20, 20), pady=(0, 10)
        )
        about_button.pack(side="left")
        help_button.pack(side="right")

    def get_save_file_path(self):
        self.savepath = filedialog.askdirectory()
        if self.savepath:
            self.filepath.set(self.savepath)

    def generate_ntrans_dictionary(self):
        pass

    def open_help_page(self):
        pass

    def select_all_ngrams(self):
        if self.select_all_checked.get():
            self.two_gram_checked.set(self.selected)
            self.three_gram_checked.set(self.selected)
            self.four_gram_checked.set(self.selected)
            self.five_gram_checked.set(self.selected)
            self.six_gram_checked.set(self.selected)
        else:
            self.two_gram_checked.set(self.deselected)
            self.three_gram_checked.set(self.deselected)
            self.four_gram_checked.set(self.deselected)
            self.five_gram_checked.set(self.deselected)
            self.six_gram_checked.set(self.deselected)
        # TODO: Deselect "select all" if any N-grams are deselected

    def open_about_window(self):
        self.about_window = AboutWindow()


class AboutWindow:
    def __init__(self):
        self.about_window = tkinter.Toplevel()
        self.about_window.resizable(False, False)
        self.about_window.title("About N-Trans")

        self.mainframe = ttk.Frame(self.about_window)
        self.mainframe.pack(fill="both", expand=True)

        header = ttk.Label(
            self.mainframe, text="About N-Trans", font=("TkDefaultFont", 18)
        )

        main_text = ttk.Label(
            self.mainframe,
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

        credit_text = ttk.Label(self.mainframe, text="Thanks to Akuli")

        header.grid(column=0, row=0, padx=(0, 0), pady=(20, 20))
        main_text.grid(sticky="W", column=0, row=1, padx=(10, 30), pady=(0, 30))
        credit_text.grid(sticky="E", column=0, row=2, padx=(0, 30), pady=(30, 10))


ntrans_gui = NTransMainGui()
ntrans_gui.root.mainloop()
