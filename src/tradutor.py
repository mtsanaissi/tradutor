from tkinter import *
from tkinter import ttk
from google.cloud import translate_v2 as translate
import time

class MyTranslatorApp:
    def __init__(self, root):
        root.title("Tradutor")
        # size and position of the window
        root.geometry("900x250+500+200")
        root.minsize(width=600, height=200)
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, padx=10)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1, minsize=100)
        mainframe.columnconfigure(4, weight=1, minsize=50)
        mainframe.rowconfigure(0, weight=1, minsize=100)

        # input text area and its vertical scroll
        self.input_text_entry = Text(mainframe, width = 140, height = 70, wrap = "word")
        input_vertical_scrollbar = ttk.Scrollbar(mainframe, orient = 'vertical', command = self.input_text_entry.yview)
        self.input_text_entry['yscrollcommand'] = input_vertical_scrollbar.set
        self.input_text_entry.grid(column = 0, row = 0, columnspan=2)
        input_vertical_scrollbar.grid(column = 2, row = 0, sticky = 'ns')

        ttk.Separator(mainframe, orient=VERTICAL).grid(column=3, row=0, sticky='ns', padx=5)

        # output text area and its vertical scroll
        self.output_text_entry = Text(mainframe, width = 140, height = 70, wrap = "word")
        output_vertical_scrollbar = ttk.Scrollbar(mainframe, orient = 'vertical', command = self.output_text_entry.yview)
        self.output_text_entry['yscrollcommand'] = output_vertical_scrollbar.set
        self.output_text_entry.grid(column = 4, row = 0, columnspan=2)
        output_vertical_scrollbar.grid(column = 6, row = 0, sticky = 'ns')

        # from language selection
        self.from_language_entry = ttk.Entry(mainframe, width=10)
        self.from_language_entry.grid(column=1, row=1, sticky='e')
        self.from_language_entry.insert(0, "en")
        
        # switch language button
        switch_language_button = ttk.Button(mainframe, text='<>', command=self.switch_language, width=4)
        switch_language_button.grid(column=2, row=1, columnspan=2, padx=3)

        # to language selection
        self.to_language_entry = ttk.Entry(mainframe, width=10)
        self.to_language_entry.grid(column=4, row=1, sticky='w')
        self.to_language_entry.insert(0, "pt-BR")
        
        # translate button
        ttk.Button(mainframe, text="Traduzir", command=self.translate).grid(column=0, row=2, columnspan=7)

        # shortcut info labels
        ttk.Label(mainframe, text="ALT+A: Selecionar texto\nALT+S: Trocar idiomas\nALT+D: Traduzir").grid(column=5, row=1, rowspan=2)

        for child in mainframe.winfo_children(): 
            child.grid_configure(pady=5)

        self.input_text_entry.focus()
        root.bind("<Alt-d>", self.translate)
        root.bind("<Alt-t>", self.translate)
        root.bind("<Alt-s>", self.switch_language)
        root.bind("<Alt-a>", self.select_focus_input_text)
    
    def translate(self, *args):
        """
        Translate text using Google Cloud Translation API
        """
        try:
            input_text = self.input_text_entry.get('1.0', 'end')
            input_text = input_text.strip()
            from_language = self.from_language_entry.get()
            to_language = self.to_language_entry.get()
            # call the Google Cloud Translation API to translate the text
            translate_client = translate.Client()
            translation = translate_client.translate(input_text, source_language=from_language, target_language=to_language)

            self.output_text_entry.delete('1.0', END)
            self.output_text_entry.insert('1.0', translation["translatedText"])
            # creative solution because running the app as an executable (built with pyinstaller),
            # the app opens a terminal window when calling the translate function. Doesn't happen running as a script.
            time.sleep(1)
            self.output_text_entry.focus()
            self.output_text_entry.tag_add("sel", "1.0", "end-1c")
        except ValueError:
            pass

    def switch_language(self, *args):
        """
        Exchange values of from and to language text boxes
        """
        from_language = self.from_language_entry.get()
        to_language = self.to_language_entry.get()
        self.from_language_entry.delete(0, END)
        self.from_language_entry.insert(0, to_language)
        self.to_language_entry.delete(0, END)
        self.to_language_entry.insert(0, from_language)
    
    def select_focus_input_text(self, *args):
        """
        Focus and select the input text. Convenient for doing a new translation.
        """
        self.input_text_entry.focus()
        self.input_text_entry.tag_add("sel", "1.0", "end-1c")

root = Tk()
root.iconphoto(True, PhotoImage(file='icon.png'))
MyTranslatorApp(root)
root.mainloop()