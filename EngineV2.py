#!/usr/local/bin/python3
######################################################################
## Imports
######################################################################

import matplotlib, DatasetFactory, Plotter, PlotWindow, PlotOptionsWindow, FileSelectionGui, FileWriter
matplotlib.use('TkAgg')

import concurrent.futures

from tkinter import filedialog
from Utils.Enums import PlotType
from Utils import ProjectUpdater
import Filters, inspect, ast

import sys, os
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

######################################################################
## EngineV2
######################################################################

class EngineV2(Tk, PlotOptionsWindow.PlotOptionInterface):
    """
    EngineV2 is the main program that runs the application.
    """

    def __init__(self):
        """
        Constructor
        @return
        """
        Tk.__init__(self)

        self.wm_title("eCLAM")
        icon = Image("photo", file="resources/icon.gif")
        self.tk.call("wm", "iconphoto", self._w, icon)

        self.multiset = None

        self.dataset = None
        self.plotter = None
        self.activePlot = None

        self.plots = {}

        self._init_splash()
        self.splash.lift()

    def _init_splash(self):
        """

        @return
        """
        self.splash = Frame(self)
        self.splash.grid(sticky=NSEW)

        # using GIF because PhotoImage doesn't support anything good
        photo = PhotoImage(file="resources/splash.gif")
        lblImg = Label(self.splash, compound=CENTER, text="", image=photo)
        lblImg.image = photo
        lblImg.grid(sticky=NSEW, pady=5)

        btnOpen = Button(self.splash, text="New Dataset", command=self._init_window)
        btnOpen.grid(sticky=NSEW, padx=5)

        btnUpdate = Button(self.splash, text="Update eCLAM", command=self.update)
        btnUpdate.grid(sticky=NSEW, padx=5)

    def _init_window(self):
        """

        @return
        """

        newWindow = Toplevel(self)
        newWindow.wm_title("eCLAM")
        newWindow.wm_geometry("800x600")
        self.main = Frame(newWindow)
        self.main.grid(sticky=NSEW)
        newWindow.grid_rowconfigure(0, weight=1)
        newWindow.grid_columnconfigure(0, weight=1)

        datasetSpecs = LabelFrame(self.main, text="Dataset Specification")
        datasetSpecs.grid(sticky=NSEW)

        self.main.grid_columnconfigure(0, weight=1)

        datasetSpecs.grid_columnconfigure(0, weight=1)
        datasetSpecs.grid_columnconfigure(1, weight=5)

        btnSelectdir = Button(datasetSpecs, text="Specify Dataset", command=self.selectDataset)
        btnSelectdir.grid(sticky=W, padx=10)

        self.lblSelectedDir = Label(datasetSpecs, text="Dataset directory not yet specified")
        self.lblSelectedDir.grid(row=0, column=1, sticky=E, padx=10)

        lowerSection = Frame(self.main, borderwidth=7)

        lowerSection.grid(sticky=NSEW)

        self.main.grid_rowconfigure(1, weight=5)

        self.sidebar = Frame(lowerSection)
        self.sidebar.grid(sticky=NSEW)

        self.plotArea = Frame(lowerSection)
        self.plotArea.grid(row=0, column=1, sticky=NSEW)
        self.plotArea.grid_columnconfigure(0, weight=1)
        self.plotArea.grid_rowconfigure(0, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        lowerSection.grid_rowconfigure(0, weight=1)
        lowerSection.grid_columnconfigure(1, weight=1)

        plots = Frame(self.sidebar, borderwidth=3)
        plots.grid(sticky=NSEW)

        lblPlots = Label(plots, text="Active Plots")
        lblPlots.grid(sticky=N)

        self.lstActivePlots = Listbox(plots)
        # Why am I using Bind??? ask Tkinter -> You have to for this widget....
        self.lstActivePlots.bind("<<ListboxSelect>>", self.updateActivePlot)
        self.lstActivePlots.bind("<Key>", self.deletePlot)
        self.lstActivePlots.grid(sticky=NSEW)

        addPltFrame = LabelFrame(plots, text="Add Plot")
        addPltFrame.grid(sticky=NSEW)

        addPltFrame.grid_rowconfigure(0, weight=1)
        addPltFrame.grid_columnconfigure(0, weight=1)
        addPltFrame.grid_rowconfigure(1, weight=1)
        addPltFrame.grid_rowconfigure(2, weight=1)

        btnSpectra = Button(addPltFrame, text="Spectrogram", command=lambda: self.generatePlot(PlotType.SPECTRA))
        btnSpectra.grid(sticky=EW, padx=5)

        # added button to indicate index of multiset to query for spectragram
        self.spectPlotNum = Spinbox(addPltFrame, from_=0, to=4, width=5)
        self.spectPlotNum.grid(row=0, column=1, sticky=EW)

        self.varShowContour = IntVar()
        chkShowCountour = Checkbutton(addPltFrame, text="Show Contour", variable=self.varShowContour)
        chkShowCountour.grid(row=0, column=2, padx=5)

        btnCycle = Button(addPltFrame, text="Cycle", command=lambda: self.generatePlot(PlotType.CYCLE_LINE))
        btnCycle.grid(sticky=EW, padx=10)

        self.spnrNumCycle = Spinbox(addPltFrame, from_=0, to=102, width=5)
        self.spnrNumCycle.grid(row=1, column=1, sticky=EW)

        btnVoltage = Button(addPltFrame, text="Voltage", command=lambda: self.generatePlot(PlotType.VOLTAGE_LINE))
        btnVoltage.grid(sticky=EW, padx=10)

        self.spnrNumVoltage = Spinbox(addPltFrame, from_=0, to=1600, width=5)
        self.spnrNumVoltage.grid(row=2, column=1, sticky=EW)

        self.voltageAverage = BooleanVar()
        self.chkVoltageGetAverage = Checkbutton(addPltFrame, text="Fill Lines", variable=self.voltageAverage)
        self.chkVoltageGetAverage.grid(row=2, column=2, padx=5)

        self.plotOptions = LabelFrame(self.sidebar, text="Plot Options")
        self.plotOptions.grid(sticky=NSEW)
        self.activePlotOptions = None

        btnExport = Button(addPltFrame, text="Export", command=lambda: self.exportCSV(self.dataset))
        btnExport.grid(sticky=EW, padx=10)

        filterOverFrame = LabelFrame(self.sidebar, text="Filter Options")
        filterOverFrame.grid(sticky=NSEW)

        filterOverFrame.columnconfigure(0, weight=10)
        filterOverFrame.columnconfigure(1, weight=1)

        canvas = Canvas(filterOverFrame)
        canvas.grid(sticky=NSEW, row=0, column=0)


        self.backgroundOptions = Frame(canvas, bd=0)


        scrollBar = Scrollbar(filterOverFrame, orient="vertical", command=canvas.yview)
        scrollBar.grid(sticky=NSEW, row=0, column=1)
        canvas.configure(yscrollcommand=scrollBar.set)

        canvas.create_window((0,0),window=self.backgroundOptions, anchor=NW)
        self.backgroundOptions.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all"), height=100))

        outputFrame = LabelFrame(self.sidebar,text="Relevant Information")
        outputFrame.grid(sticky=NSEW)

        self.txtOutput = Text(outputFrame, width=10, height=4)
        self.txtOutput.grid(sticky=NSEW)

        outputFrame.grid_columnconfigure(0, weight=1)
        outputFrame.grid_rowconfigure(0, weight=1)

        self.backgroundOptions.grid_columnconfigure(0, weight=1)
        self.backgroundOptions.grid_columnconfigure(1, weight=8)


        self.chkVarsFilters = {}
        self.filterOptions = {}
        filterCol = 0
        for name, obj in inspect.getmembers(sys.modules[Filters.BackgroundSubtraction.__module__]):
            if inspect.isclass(obj) and issubclass(obj, Filters.Filter):
                if name != "Filter":
                    self.chkVarsFilters[name] = IntVar()
                    self.filterOptions[name] = obj
                    args, vargs, keys, defaults = inspect.getargspec(obj)
                    # print(args)
                    temp = Checkbutton(self.backgroundOptions, text=name, variable=self.chkVarsFilters[name], command=self.filtersChanged)
                    temp.grid(column=1, row=filterCol, sticky=NSEW)
                    filterCol = filterCol + 1

    def update(self):
        version = ProjectUpdater.getCurrentVersion()
        version.update()
        print("Update Complete")

    def filtersChanged(self):
        """

        @return
        """
        if self.plotter == None:
            return
        if not'filtersetStack' in vars(self):
            self.filtersetStack = []
        filterStack = self.dataset
        for className in self.filterOptions.keys():
            if self.chkVarsFilters[className].get():
                if not className in self.filtersetStack:
                    self.filtersetStack.append(className)
            else:
                if className in self.filtersetStack:
                    self.filtersetStack.remove(className)

        for className in self.filtersetStack:
            filterStack = filterStack.applyFilter(self.filterOptions[className])
            print("Applying Filter: %s" % (className))
        self.plotter.updateData(filterStack)
        self.updateView()

    def updateText(self,text):
        self.txtOutput.delete(1.0, END)
        self.txtOutput.insert(END, text)

    def updateActivePlot(self, event):
        """

        @param event:
        @return
        """
        self.activePlot = list(self.plots.keys())[self.lstActivePlots.curselection()[0]]
        self.updateView()

    ###################################################
    ## SELECT DATASET
    ###################################################

    def selectDataset(self):
        """
        Initializes the dataset variable using the datasetfactory
        static method.

        @return
        """

        # changing the function of this to allow for input of multiple datasets
        # instead of quitting once a directory is selected, it will continue to
        # prompt the user until they hit cancel
        # once cancel is selected, all previous entries will have been saved into
        # the multiset
        self.fileSelector = FileSelectionGui.FileSelectionGui(self, self)


    def updateView(self):
        """

        @return
        """
        self.lstActivePlots.delete(0, END)
        for k in self.plots.keys():
            self.lstActivePlots.insert(END, k)
        if self.activePlot != None:
            if self.activePlotOptions != None:
                self.activePlotOptions.destroy()
            curPoint = None
            # This is a hack if I ever saw one
            if len(self.activePlot.split("pt")) > 1:
                curPoint = int(self.activePlot.split("pt")[1])
            self.activePlotOptions = PlotOptionsWindow.createPlotOptionsFromPlotWindow(self.plotOptions, self.plots[self.activePlot], self, self.plotter.getDataset(), plotPoint=curPoint)
            self.activePlotOptions.grid(sticky=NSEW)
            self.lstActivePlots.select_set(list(self.plots.keys()).index(self.activePlot))
            self.plots[self.activePlot].grid(row=0, column=0, sticky=NSEW)
            self.plots[self.activePlot].tkraise()
        if self.plotter != None:
            self.updateText(str(self.plotter))

    def deletePlot(self, event):
        """

        @param event:
        @return
        """
        # TODO: Make sure this is cross platform
        if event.keycode == 3342463:
            self.plots[self.activePlot].destroy()
            del self.plots[self.activePlot]
            if len(self.plots.keys()) > 0:
                self.activePlot = list(self.plots.keys())[0]
            else:
                self.activePlot = None
            self.updateView()

    def generatePlot(self, type, point=-1):
        """
        @param option:
        @param type:
        @param point:
        @return
        """
        self.plotter.dataset.setAverageDataset(bool(self.voltageAverage.get()))
        if type == PlotType.SPECTRA:
            self.dataset.setCurrentIndex(int(self.spectPlotNum.get()))
            self.plots["Spectra " + str(self.dataset)] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createSpectra(contour=1 if self.varShowContour.get() else 0, index=int(self.spectPlotNum.get())), type)
            self.activePlot = "Spectra " + str(self.dataset.currentDataset)

        elif type == PlotType.VOLTAGE_LINE:

            value = point if point != -1 else int(self.spnrNumVoltage.get())
            self.activePlot = "Voltage - pt" + str(value)
            self.plots[self.activePlot] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createYPointPlot(value), type)

        elif type == PlotType.CYCLE_LINE:
            value = point if point != -1 else int(self.spnrNumCycle.get())
            self.activePlot = "Cycle - pt" + str(value)
            self.plots[self.activePlot] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createXPointPlot(value), type)

        else:
            raise Exception("Unknown Plot type")

        self.updateView()

    def exportCSV(self, dataset):
        """

        @return
        """
        outputDir = filedialog.askdirectory()
        if os.path.isdir(outputDir):
            FileWriter.write_csv(outputDir, dataset)
        else:
            print("did not export to:" + outputDir)

    def loadConfig(self):
        """

        @return
        """
        self.fileSelector = FileSelectionGui.FileSelectionGui(self, self)


    def handleFileSelectionResponce(self, fileList, recognizer):
        """

        @param fileList:
        @return
        """

        if len(fileList) == 0:
            self.lblSelectedDir.configure(text="Dataset directory not yet specified")
            return
        if len(fileList) > 1:
            self.lblSelectedDir.configure(text="Multiple Directories selected - data is of type %s" % (str(recognizer)))
        else:
            self.lblSelectedDir.configure(text="Single Dataset Selected - data is of type %s" % (str(recognizer)))

        self.dataset = DatasetFactory.buildMultiset()

        with concurrent.futures.ThreadPoolExecutor() as tpe:
            dsFutures = []
            for i in fileList.keys():
                dsFutures.append(tpe.submit(lambda x: DatasetFactory.buildDataset(fileList[x],
                                                                                  ast.literal_eval(x),
                                                                                  hint=recognizer), i))
            for ff in dsFutures:
                self.dataset.addDataset(ff.result())

        self.plotter = Plotter.Plotter(self.dataset)

    def createSpectraWithYHighlight(self, point):
        """

        @param point:
        @return
        """
        self.plots["Spectra highlight " + str(point)] = \
            PlotWindow.PlotWindow(self.plotArea, self.plotter.createSpectra(
                yHighlight=point, contour=1 if self.varShowContour.get() else 0), PlotType.SPECTRA)
        self.activePlot = "Spectra highlight " + str(point)
        self.updateView()

    def createSpectraWithXHighlight(self, point):
        """

        @param point:
        @return
        """
        self.plots["Spectra highlight " + str(point)] = \
            PlotWindow.PlotWindow(self.plotArea, self.plotter.createSpectra(
                xHighlight=point, contour=1 if self.varShowContour.get() else 0), PlotType.SPECTRA)
        self.activePlot = "Spectra highlight " + str(point)
        self.updateView()

    def createXPlot(self, cycle):
        """

        @param cycle:
        @return
        """
        self.generatePlot(PlotType.CYCLE_LINE, point=cycle)

    def createYPlot(self, point):
        """

        @param point:
        @return
        """
        self.generatePlot(PlotType.VOLTAGE_LINE, point=point)



######################################################################
## Main
######################################################################

if __name__ == "__main__":
    engine = EngineV2()
    engine.mainloop()
