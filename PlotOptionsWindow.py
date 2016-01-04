
import sys, PlotWindow, Utils.Calculations
from Utils.Enums import PlotType
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

class PlotOptionInterface():

    def createSpectraWithYHighlight(self, point):
        raise NotImplementedError()

    def createSpectraWithXHighlight(self, point):
        raise NotImplementedError()

    def createXPlot(self, cycle):
        raise NotImplementedError()

    def createYPlot(self, point):
        raise NotImplementedError()

class PlotOptions(Frame):
    def __init__(self, parent, handler: PlotOptionInterface, dataset, plotPoint=None):
        super().__init__(parent)
        self.handler = handler
        self.plotPoint = plotPoint
        print("Created PlotOptions " + str(self.plotPoint))
        self.init_window(dataset)

    def init_window(self):
        raise NotImplementedError()


class SpectraPlotOptions(PlotOptions):
    def init_window(self, dataset):
        btnCreateCycleMax = Button(self, text="Create Cycle from MAX Im",
                                   command=lambda :self.handler.createXPlot(Utils.Calculations.getXAtMaxIm(dataset)))
        btnCreateCycleMax.grid(sticky=NSEW)

        btnCreateCycleMin = Button(self, text="Create Cycle from MIN Im",
                                   command=lambda :self.handler.createXPlot(Utils.Calculations.getXAtMinIm(dataset)))
        btnCreateCycleMin.grid(sticky=NSEW)

        btnCreateVoltMax = Button(self, text="Create Voltage from MAX Im",
                                  command=lambda :self.handler.createYPlot(Utils.Calculations.getYAtMaxIm(dataset)))
        btnCreateVoltMax.grid(sticky=NSEW)

        btnCreateVoltMin = Button(self, text="Create Voltage from MIN Im",
                                  command=lambda :self.handler.createYPlot(Utils.Calculations.getYAtMinIm(dataset)))
        btnCreateVoltMin.grid(sticky=NSEW)

class CyclePlotOptions(PlotOptions):
    def init_window(self, dataset):
        btnViewSpectraMax = Button(self, text="View MAX Im on Spectra",
                                   command=lambda :self.handler.createSpectraWithYHighlight(Utils.Calculations.getYFromMaxImAtX(dataset, self.plotPoint)))
        btnViewSpectraMax.grid(sticky=NSEW)

        btnViewSpectraMin = Button(self, text="View MIN Im on Spectra",
                                   command=lambda :self.handler.createSpectraWithYHighlight(Utils.Calculations.getYFromMinImAtX(dataset, self.plotPoint)))
        btnViewSpectraMin.grid(sticky=NSEW)

        btnCreateVoltMax = Button(self, text="Create Voltage from MAX Im",
                                  command=lambda :self.handler.createYPlot(Utils.Calculations.getYAtMaxIm(dataset)))
        btnCreateVoltMax.grid(sticky=NSEW)

        btnCreateVoltMin = Button(self, text="Create Voltage from MIN Im",
                                  command=lambda :self.handler.createYPlot(Utils.Calculations.getYAtMinIm(dataset)))
        btnCreateVoltMin.grid(sticky=NSEW)


class VoltagePlotOptions(PlotOptions):
    def init_window(self, dataset):
        btnViewSpectraMax = Button(self, text="View MAX Im on Spectra",
                                   command=lambda :self.handler.createSpectraWithXHighlight(Utils.Calculations.getXFromMaxImAtY(dataset, self.plotPoint)))
        btnViewSpectraMax.grid(sticky=NSEW)

        btnViewSpectraMin = Button(self, text="View MIN Im on Spectra",
                                   command=lambda :self.handler.createSpectraWithXHighlight(Utils.Calculations.getXFromMinImAtY(dataset, self.plotPoint)))
        btnViewSpectraMin.grid(sticky=NSEW)

        btnCreateCycleMax = Button(self, text="Create Cycle from MAX Im",
                                   command=lambda :self.handler.createXPlot(Utils.Calculations.getXAtMaxIm(dataset)))
        btnCreateCycleMax.grid(sticky=NSEW)

        btnCreateCycleMin = Button(self, text="Create Cycle from MIN Im",
                                  command=lambda :self.handler.createXPlot(Utils.Calculations.getXAtMinIm(dataset)))
        btnCreateCycleMin.grid(sticky=NSEW)


def createPlotOptionsFromPlotWindow(parent, plotwindow, eventHandler, dataset, plotPoint=None):
    if plotwindow.getPlotType() == PlotType.SPECTRA:
        return SpectraPlotOptions(parent, eventHandler, dataset)
    elif plotwindow.getPlotType() == PlotType.CYCLE_LINE:
        print("Passed in point " + str(plotPoint))
        return  CyclePlotOptions(parent, eventHandler, dataset, plotPoint=plotPoint)
    elif plotwindow.getPlotType() == PlotType.VOLTAGE_LINE:
        return VoltagePlotOptions(parent, eventHandler, dataset, plotPoint=plotPoint)
    else:
        raise Exception("Unknown plot type: " + str(plotwindow.getPlotType()))