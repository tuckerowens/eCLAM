
######################################################################
## Imports
######################################################################

import sys, Utils.Calculations
from Utils.Enums import PlotType
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

######################################################################
## PlotOptionInterface
######################################################################

class PlotOptionInterface():
    """

    """

    def createSpectraWithYHighlight(self, point):
        """

        @param point:
        @return
        """
        raise NotImplementedError()

    def createSpectraWithXHighlight(self, point):
        """

        @param point:
        @return
        """
        raise NotImplementedError()

    def createXPlot(self, cycle):
        """

        @param cycle:
        @return
        """
        raise NotImplementedError()

    def createYPlot(self, point):
        """

        @param point:
        @return
        """
        raise NotImplementedError()

######################################################################
## PlotOptions
######################################################################

class PlotOptions(Frame):
    """

    """
    def __init__(self, parent, handler: PlotOptionInterface, dataset, plotPoint=None):
        """

        @param parent:
        @param handler:
        @param dataset:
        @param plotPoint:
        @return
        """
        super().__init__(parent)
        self.handler = handler
        self.plotPoint = plotPoint
        self.init_window(dataset)

    def init_window(self):
        """

        @return
        """
        raise NotImplementedError()

######################################################################
## SpectraPlotOptions
######################################################################

class SpectraPlotOptions(PlotOptions):
    """

    """
    def init_window(self, dataset):
        """

        @param dataset:
        @return
        """
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

######################################################################
## CyclePlotOptions
######################################################################

class CyclePlotOptions(PlotOptions):
    """

    """
    def init_window(self, dataset):
        """

        @param dataset:
        @return
        """
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


######################################################################
## VoltagePlotOptions
######################################################################

class VoltagePlotOptions(PlotOptions):
    """

    """
    def init_window(self, dataset):
        """

        @param dataset:
        @return
        """
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


######################################################################
## createPlotOptionsFromPlotWindow
######################################################################

def createPlotOptionsFromPlotWindow(parent, plotwindow, eventHandler, dataset, plotPoint=None):
    """

    @param parent:
    @param plotwindow:
    @param eventHandler:
    @param dataset:
    @param plotPoint:
    @return
    """
    if plotwindow.getPlotType() == PlotType.SPECTRA:
        return SpectraPlotOptions(parent, eventHandler, dataset)
    elif plotwindow.getPlotType() == PlotType.CYCLE_LINE:
        print("Passed in point " + str(plotPoint))
        return  CyclePlotOptions(parent, eventHandler, dataset, plotPoint=plotPoint)
    elif plotwindow.getPlotType() == PlotType.VOLTAGE_LINE:
        return VoltagePlotOptions(parent, eventHandler, dataset, plotPoint=plotPoint)
    else:
        raise Exception("Unknown plot type: " + str(plotwindow.getPlotType()))
