

from tkinter import filedialog

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *



class FileSelectionGui(Toplevel):

    def __init__(self, tk, fileSelectorResponce):
        Toplevel.__init__(self)
        self.wm_title("Dataset Specification Assistant")
        self.wm_geometry("480x360")
        self.handler = fileSelectorResponce
        self.main = Frame(self)
        self.main.grid(sticky=NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btnSelectDir = Button(self.main, text="Select a Dataset root", command=self.directorySelected)
        btnSelectDir.grid(sticky=N)
        print("Built File Selection")


    def directorySelected(self):
        selected = filedialog.askdirectory()
        if selected == "":
            return
        self.handler.handleFileSelectionResponce(selected)

