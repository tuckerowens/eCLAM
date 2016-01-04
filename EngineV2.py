#!/usr/local/bin/python3

import matplotlib, DatasetFactory, Plotter, PlotWindow, PlotOptionsWindow
matplotlib.use('TkAgg')

import Filters

import PIL
from PIL import ImageTk
from tkinter import filedialog
from Utils.Enums import PlotType

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *



class EngineV2(Tk, PlotOptionsWindow.PlotOptionInterface):

    def __init__(self):
        Tk.__init__(self)

        self.wm_title("eCLAM")
        icon = Image("photo", file="resources/icon.gif")
        self.tk.call("wm", "iconphoto", self._w, icon)


        self.dataset = None
        self.plotter = None
        self.activePlot = None

        self.plots = {}

        self._init_splash()
        self.splash.lift()


    def _init_splash(self):
        self.splash = Frame(self)
        self.splash.grid(sticky=NSEW)


        # using GIF because PhotoImage doesn't support anything good
        photo = PhotoImage(file="resources/splash.gif")
        lblImg = Label(self.splash, compound = CENTER, text="", image=photo)
        lblImg.image = photo
        lblImg.grid(sticky=NSEW, pady=5)

        btnOpen = Button(self.splash, text="New Dataset", command=self._init_window)
        btnOpen.grid(sticky=NSEW, padx=5)

        btnLoad = Button(self.splash, text="Load Existing eCLAM Config", command=self.loadConfig)
        btnLoad.grid(sticky=NSEW, padx=5)

    def _init_window(self):
        newWindow = Toplevel(self)
        newWindow.wm_title("eCLAM")
        newWindow.wm_geometry("640x480")
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
        btnSpectra.grid(sticky=EW, padx=10, columnspan=2)


        btnCycle = Button(addPltFrame, text="Cycle", command=lambda: self.generatePlot(PlotType.CYCLE_LINE))
        btnCycle.grid(sticky=EW, padx=10)
        self.spnrNumCycle = Spinbox(addPltFrame, from_=0, to=102, width=5)
        self.spnrNumCycle.grid(row=1, column=1, sticky=EW)

        btnVoltage = Button(addPltFrame, text="Voltage", command=lambda: self.generatePlot(PlotType.VOLTAGE_LINE))
        btnVoltage.grid(sticky=EW, padx=10)
        self.spnrNumVoltage = Spinbox(addPltFrame, from_=0, to=102, width=5)
        self.spnrNumVoltage.grid(row=2, column=1, sticky=EW)

        self.plotOptions = LabelFrame(self.sidebar, text="Plot Options")
        self.plotOptions.grid(sticky=NSEW)
        self.activePlotOptions = None

        self.backgroundOptions = LabelFrame(self.sidebar, text="Background Configuration")
        self.backgroundOptions.grid(sticky=NSEW)

        self.chkVarAddBg = IntVar()
        chkAddBackground = Checkbutton(self.backgroundOptions, text="Apply Background subtraction", variable=self.chkVarAddBg, command=self.applyBgChanged)
        chkAddBackground.grid(sticky=NSEW)


    def applyBgChanged(self):
        if self.plotter == None:
            return
        if self.chkVarAddBg.get():
            self.plotter.updateData(Filters.BackgroundSubtraction(self.dataset))
        else:
            self.plotter.updateData(self.dataset)

    def updateActivePlot(self, event):
        self.activePlot = list(self.plots.keys())[self.lstActivePlots.curselection()[0]]
        self.updateView()

    def selectDataset(self):
        selected = filedialog.askdirectory()
        self.lblSelectedDir.configure(text=selected)
        self.dataset = DatasetFactory.buildDataset(selected + '/')
        self.plotter = Plotter.Plotter(self.dataset)

    def updateView(self):
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

    def deletePlot(self, event):
        if event.keycode == 3342463:
            self.plots[self.activePlot].destroy()
            del self.plots[self.activePlot]
            if len(self.plots.keys()) > 0:
                self.activePlot = list(self.plots.keys())[0]
            else:
                self.activePlot = None
            self.updateView()


    def generatePlot(self, type, point=-1):
        if type == PlotType.SPECTRA:
            self.plots["Spectra"] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createSpectra(), type)
            self.activePlot = "Spectra"
        elif type == PlotType.VOLTAGE_LINE:
            value =  point if point != -1 else int(self.spnrNumVoltage.get())
            self.activePlot = "Voltage - pt" + str(value)
            self.plots[self.activePlot] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createYPointPlot(value), type)
        elif type == PlotType.CYCLE_LINE:
            value = point if point != -1 else int(self.spnrNumCycle.get())
            self.activePlot = "Cycle - pt" + str(value)
            self.plots[self.activePlot] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createXPointPlot(value), type)

        else:
            raise Exception("Unknown Plot type")
        self.updateView()




    def loadConfig(self):
        #load file
        self._init_window()

    def createSpectraWithYHighlight(self, point):
        self.plots["Spectra highlight " + str(point)] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createSpectra(yHighlight=point), PlotType.SPECTRA)
        self.activePlot = "Spectra highlight " + str(point)
        self.updateView()

    def createSpectraWithXHighlight(self, point):
        self.plots["Spectra highlight " + str(point)] = PlotWindow.PlotWindow(self.plotArea, self.plotter.createSpectra(xHighlight=point), PlotType.SPECTRA)
        self.activePlot = "Spectra highlight " + str(point)
        self.updateView()

    def createXPlot(self, cycle):
        self.generatePlot(PlotType.CYCLE_LINE, point=cycle)

    def createYPlot(self, point):
        self.generatePlot(PlotType.VOLTAGE_LINE, point=point)



if __name__ == "__main__":
    engine = EngineV2()
    engine.mainloop()