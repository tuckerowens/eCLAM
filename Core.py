import matplotlib, DatasetFactory, Plotter, PlotWindow
matplotlib.use('TkAgg')


from tkinter import filedialog
import Filters

from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *



class Core(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.wm_title("eCLAM")
        self.wm_geometry("480x400")


        self.dataset = None
        self.plotter = None
        self.lastSelectedPlot = 0

        self._init_window()
        self.base.lift()


    def _init_window(self):

        self.base = Frame(self)
        self.base.pack(fill=BOTH, expand=1)


        loadOptions = LabelFrame(self.base, text="Load options")
        loadOptions.pack(fill=X, padx=10, pady=5)


        self.selectedDir = Label(loadOptions, text="")
        self.selectedDir.pack(side=LEFT)

        self.browse = Button(loadOptions, text="Load Data", command=self._setDirectory)
        self.browse.pack(side=LEFT)


        viewOptions = LabelFrame(self.base, text="View")
        viewOptions.pack(fill=X, padx=10)


        self.btnViewSpectro = Button(viewOptions, text="Spectrogram", command=lambda :self._showPlot(0))
        self.btnViewSpectro.pack(side=LEFT)

        self.btnViewPoint = Button(viewOptions, text="Point", command=lambda :self._showPlot(1))
        self.btnViewPoint.pack(side=LEFT)

        self.btnViewCycle = Button(viewOptions, text="Cycle", command=lambda :self._showPlot(2))
        self.btnViewCycle.pack(side=LEFT)

        controls = LabelFrame(self.base, text="General Controls")
        controls.pack(fill=X, padx=10)

        self.plotWindow = Frame(self.base)

        self.voltagePoint = IntVar()
        self.cyclePoint = IntVar()
        self.filterSetAppy = IntVar()

        self.chkApplyFilterSet = Checkbutton(controls, text="Apply Filter Set", variable=self.filterSetAppy, command=lambda : self.updatePlots(1))
        self.chkApplyFilterSet.pack(side=LEFT)

        self.sldVoltagePoint = Scale(controls, orient=HORIZONTAL, label="Voltage Point", from_=0, to=1600, variable=self.voltagePoint, command=self.updatePlots)
        self.sldVoltagePoint.pack(side=LEFT, fill=X, pady=5, expand=True)

        self.sldCyclePoint = Scale(controls, orient=HORIZONTAL, label="Cycle Number", from_=0, to=102, variable=self.cyclePoint, command=self.updatePlots)
        self.sldCyclePoint.pack(side=LEFT, fill=X, pady=5, expand=True)


        self.plotWindow.config(bg="black")
        self.plotWindow.pack()


    def _setDirectory(self):
        selected = filedialog.askdirectory()
        self.selectedDir.configure(text=selected)
        self.dataset = DatasetFactory.buildDataset(selected + '/')
        self.plotter = Plotter.Plotter(self.dataset)
        self._plotDataset()


    def updatePlots(self, event):
        if self.plotter == None:
            return
        if self.filterSetAppy.get():
            self.plotter.updateData(Filters.BackgroundSubtraction(self.dataset))
        else:
            self.plotter.updateData(self.dataset)
        self.specra = PlotWindow.PlotWindow(self.plotWindow, self.plotter.createSpectra())
        self.lineHoriz = PlotWindow.PlotWindow(self.plotWindow, self.plotter.createYPointPlot(self.voltagePoint.get()))
        self.lineVert = PlotWindow.PlotWindow(self.plotWindow, self.plotter.createXPointPlot(self.cyclePoint.get()))
        self._showPlot(self.lastSelectedPlot)



    def _showPlot(self, event):
        self.lastSelectedPlot = event
        if (event == 0):
            self.specra.grid(row=0, column=0)
            self.specra.tkraise()
        elif(event == 1):
            self.lineHoriz.grid(row=0, column=0)
            self.lineHoriz.tkraise()
        elif(event == 2):
            self.lineVert.grid(row=0, column=0)
            self.lineVert.tkraise()
        else:
            raise Exception("Unknown Event code " +  str(event))

    def _plotDataset(self):
        self.specra = PlotWindow.PlotWindow(self.plotWindow, self.plotter.createSpectra())
        self.lineHoriz = PlotWindow.PlotWindow(self.plotWindow, self.plotter.createYPointPlot(self.cyclePoint.get()))
        self.lineVert = PlotWindow.PlotWindow(self.plotWindow, self.plotter.createXPointPlot(self.voltagePoint.get()))






app = Core()
app.mainloop()