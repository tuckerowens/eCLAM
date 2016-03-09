

from tkinter import filedialog
from Utils.FileRecognizer import *

import sys, os
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

        top = self.winfo_toplevel()
        self.menuBar = Menu(top)
        top['menu'] = self.menuBar

        self.subMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Configure', menu=self.subMenu)
        self.subMenu.add_command(label='Set Config', command=self.__handleSetConfig)
        self.configFile = "resources/defaultFileRecognizers.xml"

        self.lstBoxes = {}
        self.frameBoxes = {}

        dirBox = LabelFrame(self.main, text="Selected Dataset")
        dirBox.grid(sticky=NSEW, padx=5)
        self.main.grid_columnconfigure(0, weight=1)

        self.selectedDir = Label(dirBox, text="No directory selected")
        self.selectedDir.grid(sticky=NSEW)
        btnSelectDir = Button(dirBox, text="Browse", command=self.directorySelected)
        btnSelectDir.grid(row=0, column=1, sticky=E)
        dirBox.grid_columnconfigure(0, weight=5)
        dirBox.grid_columnconfigure(1, weight=1)

        fileTypesFrame = LabelFrame(self.main, text="Matching File Types")
        fileTypesFrame.grid(sticky=NSEW, padx=5)
        self.lstFileTypes = Listbox(fileTypesFrame, exportselection=0)
        self.lstFileTypes.bind("<<ListboxSelect>>", self.fileTypeSelected)
        self.lstFileTypes.grid(sticky=NSEW, padx=2)
        fileTypesFrame.grid_rowconfigure(0, weight=1)
        fileTypesFrame.grid_columnconfigure(0, weight=1)

        self.componentFrame = LabelFrame(self.main, text="File Components")
        self.componentFrame.grid(sticky=NSEW)
        fileTypesFrame.grid(sticky=NSEW, padx=5)
        self.main.grid_rowconfigure(1, weight=0)
        self.main.grid_rowconfigure(2, weight=5)

        btnOkay = Button(self.main, text="Okay", command=self.submit)
        btnOkay.grid(sticky=E)


    def __handleSetConfig(self):
        selected = filedialog.askopenfilename(filetypes=[("XML File", ".xml")])
        if selected == "":
            return
        self.configFile = selected



    def submit(self):
        print ("Create dataset")


    def directorySelected(self):
        selected = filedialog.askdirectory()
        if selected == "":
            return
        self.selectedDir.configure(text=selected)
        self.fileTypes = {}
        for dirpath, dirname, filenames in os.walk(selected):
            temp =  XmlFileRecognizer.recognizeBatch([f for f in filenames],self.configFile)
            for key in temp.keys():
                if key in self.fileTypes.keys():
                    self.fileTypes[key] = self.fileTypes[key]+temp[key]
                else:
                    self.fileTypes[key] = temp[key]

        for f in self.fileTypes.keys():
            self.lstFileTypes.insert(END, str(f))

    def fileTypeSelected(self, index):
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        print(cls)
        elements = {}
        for f in self.fileTypes[cls]:
            temp = cls.componentExtraction(f)
            for k in temp.keys():
                if k in elements.keys():
                    elements[k].add(temp[k])
                else:
                    elements[k] = set()
                    elements[k].add(temp[k])
        for k in elements.keys():
            if k in self.lstBoxes.keys() or k == 'fileno':
                print(k + " already built")
            else:
                self.frameBoxes[k] = LabelFrame(self.componentFrame, text=k)
                self.frameBoxes[k].grid(row=int(2+((len(self.frameBoxes.keys())-1)/3)), column=(len(self.frameBoxes.keys())-1)%3, sticky=NSEW)
                self.lstBoxes[k] = Listbox(self.frameBoxes[k], exportselection=0)
                self.lstBoxes[k].bind("<<ListboxSelect>>", self.optionSelected)
                self.lstBoxes[k].grid(sticky=NSEW)
                self.frameBoxes[k].grid_columnconfigure(0, weight=1)
                self.frameBoxes[k].grid_rowconfigure(0, weight=1)
                for item in elements[k]:
                    self.lstBoxes[k].insert(END, str(item))
                if len(elements[k]):
                    self.lstBoxes[k].selection_set(0)

    def optionSelected(self, event):
        for k in self.lstBoxes.keys():
            print(k + str(self.lstBoxes[k]))
