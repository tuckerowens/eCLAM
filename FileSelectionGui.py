

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
        self.wm_geometry("640x700")
        self.handler = fileSelectorResponce
        self.main = Frame(self)
        self.main.grid(sticky=NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = self.winfo_toplevel()
        self.menuBar = Menu(top)
        top['menu'] = self.menuBar

        self.fileset = []

        self.subMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label='File', menu=self.subMenu)
        self.subMenu.add_command(label='Load Recognizers', command=self.__handleSetConfig)
        self.subMenu.add_command(label='Set Selections as Default', command=self.__handleSaveSelection)
        self.subMenu.add_command(label='Save', command=self.__handleConfigSave)
        self.subMenu.add_command(label='Save As', command=self.__handleNewConfigSave)
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

        self.varMatcherRegexStr = StringVar()
        self.varMatcherRegexStr.trace('w', self.__handleRegexModify)
        txtRegexText = Entry(self.main, textvariable=self.varMatcherRegexStr, state=DISABLED)
        txtRegexText.grid(sticky=NSEW)

        self.componentFrame = LabelFrame(self.main, text="File Components")
        self.componentFrame.grid(sticky=NSEW)
        fileTypesFrame.grid(sticky=NSEW, padx=5)
        self.main.grid_rowconfigure(1, weight=0)
        self.main.grid_rowconfigure(2, weight=5)

        self.componentFrame.grid_columnconfigure(0, weight=1)
        self.componentFrame.grid_columnconfigure(2, weight=1)
        self.componentFrame.grid_columnconfigure(1, weight=1)

        self.componentFrame.grid_rowconfigure(0, weight=1)
        self.componentFrame.grid_rowconfigure(1, weight=1)


        bottomPanel = Frame(self.main)
        bottomPanel.grid(sticky=NSEW)

        bottomPanel.grid_columnconfigure(0, weight=4)
        bottomPanel.grid_columnconfigure(1, weight=1)

        self.lblInfo = Label(bottomPanel, text="")
        self.lblInfo.grid(sticky=W)

        btnOkay = Button(bottomPanel, text="Okay", command=self.submit)
        btnOkay.grid(column=1, row=0, sticky=E)


    def __handleSetConfig(self):
        selected = filedialog.askopenfilename(filetypes=[("XML File", ".xml")])
        if selected == "":
            return
        self.configFile = selected

    def __handleConfigSave(self):
        XmlFileRecognizer.outputToFile(self.configFile)

    def __handleNewConfigSave(self):
        newFile = filedialog.asksaveasfilename()
        if newFile == "":
            return
        self.configFile = newFile
        self.__handleConfigSave()

    def __handleRegexModify(self, x, v, g):
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        cls.updateMatcherRegex(self.varMatcherRegexStr.get())

    def __handleSaveSelection(self):
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        query = {}
        for k in self.lstBoxes.keys():
            box = self.lstBoxes[k]
            selections = box.curselection()
            query[k] = []
            for s in selections:
                query[k].append(self.elementSet[k][s])
        cls.setDefaultSelection(query)


    def submit(self):
        results = {}
        queries = [{}]
        for k in self.lstBoxes.keys():
            box = self.lstBoxes[k]
            selections = box.curselection()
            subQuery = queries
            queries = []
            query = {}
            for s in selections:
                for q in subQuery:
                    queries.append(dict(list(q.items()) + list({k: [self.elementSet[k][s]]}.items())))
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        for exp in queries:
            temp_set = list(filter(lambda x: cls.validFile(x, exp), self.fileTypes[cls]))
            if len(temp_set) > 0:
                results[str(exp)] = temp_set
        for k in results:
            results[k] = list(sorted(results[k], key=lambda x: int(cls.componentExtraction(x)['fileno'])))
        self.handler.handleFileSelectionResponce(results)


    def directorySelected(self):
        selected = filedialog.askdirectory()
        if selected == "":
            return
        self.selectedDir.configure(text=selected)
        self.fileTypes = {}
        self.fileset = []
        for dirpath, dirname, filenames in os.walk(selected):
            temp =  XmlFileRecognizer.recognizeBatch([os.path.join(dirpath, f) for f in filenames],self.configFile)
            for key in temp.keys():
                self.fileset = self.fileset +  temp[key]
                if key in self.fileTypes.keys():
                    self.fileTypes[key] = self.fileTypes[key]+temp[key]
                else:
                    self.fileTypes[key] = temp[key]

        for f in self.fileTypes.keys():
            self.lstFileTypes.insert(END, str(f))


    def updateCounts(self):
        queries = [{}]
        for k in self.lstBoxes.keys():
            box = self.lstBoxes[k]
            selections = box.curselection()
            subQuery = queries
            queries = []
            query = {}
            for s in selections:
                for q in subQuery:
                    queries.append(dict(list(q.items()) + list({k: [self.elementSet[k][s]]}.items())))
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        expCount = 0
        minCount = float("inf")
        maxCount =  0
        for exp in queries:
            temp_set = list(filter(lambda x: cls.validFile(x, exp), self.fileTypes[cls]))
            if len(temp_set) > 0:
                expCount = expCount + 1
                minCount = min(minCount, len(temp_set))
                maxCount = max(maxCount, len(temp_set))
        if minCount == maxCount:
            countString = str(minCount)
        elif maxCount == 0:
            countString = "0"
        else:
            countString = "%i-%i" % (minCount, maxCount)
        self.lblInfo.config(text="Experiment Count: %i; File Range: %s" % (expCount, countString))

    def fileTypeSelected(self, index, fileset=None):
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        self.elementSet = {}
        files = self.fileTypes[cls] if fileset == None else fileset
        self.fileset = self.fileTypes[cls] if fileset == None else fileset
        self.varMatcherRegexStr.set(cls.getMatcherRegex())
        for f in files:
            temp = cls.componentExtraction(f)
            for k in temp.keys():
                if k in self.elementSet.keys():
                    self.elementSet[k].add(temp[k])
                else:
                    self.elementSet[k] = set()
                    self.elementSet[k].add(temp[k])

        for k in self.elementSet.keys():
            self.elementSet[k] = list(self.elementSet[k])
            sorted(self.elementSet[k])

            if k in self.lstBoxes.keys() or k == 'fileno':
                if k == 'fileno': continue
                self.lstBoxes[k].delete(0,END)
                for item in sorted(list(self.elementSet[k])):
                    self.lstBoxes[k].insert(END, str(item))
                defaults = cls.getDefaultSelection()
                if k in defaults.keys():
                    if defaults[k] == "": continue
                    for l in eval(str(defaults[k])):
                        self.lstBoxes[k].selection_set(self.elementSet[k].index(l))

            else:
                self.frameBoxes[k] = LabelFrame(self.componentFrame, text=k)
                self.frameBoxes[k].grid(row=int(2+((len(self.frameBoxes.keys())-1)/3)), column=(len(self.frameBoxes.keys())-1)%3, sticky=NSEW)
                self.lstBoxes[k] = Listbox(self.frameBoxes[k], exportselection=0, selectmode=MULTIPLE)
                self.lstBoxes[k].bind("<<ListboxSelect>>", self.optionSelected)
                self.lstBoxes[k].grid(sticky=NSEW)
                self.frameBoxes[k].grid_columnconfigure(0, weight=1)
                self.frameBoxes[k].grid_rowconfigure(0, weight=1)
                self.lstBoxes[k].delete(0,END)
                for item in sorted(list(self.elementSet[k])):
                    self.lstBoxes[k].insert(END, str(item))
                defaults = cls.getDefaultSelection()
                if k in defaults.keys():
                    if defaults[k] == "": continue
                    for l in eval(str(defaults[k])):
                        self.lstBoxes[k].selection_set(self.elementSet[k].index(l))


    def optionSelected(self, event):
        query = {}
        for k in self.lstBoxes.keys():
            box = self.lstBoxes[k]
            selections = box.curselection()
            # if len(selections) == 0 or len(self.elementSet[k]) < 1: continue
            query[k] = []
            for s in selections:
                query[k].append(self.elementSet[k][s])
        cls = list(self.fileTypes.keys())[self.lstFileTypes.curselection()[0]]
        self.fileset = list(filter(lambda x: cls.validFile(x, query), self.fileTypes[cls]))
        self.updateCounts()


