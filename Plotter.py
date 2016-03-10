
######################################################################
## Imports
######################################################################

import matplotlib
import numpy as np
from matplotlib.figure import Figure

######################################################################
## Plotter
######################################################################

class Plotter:
    """
    This is the class that handles plotting of graphs.

    @field dataset: Variable containing the data to be plotted
    """

    def __init__(self, dataset):
        """
        Constructor

        :param dataset: The dataset to be plotted
        :return: null
        """
        self.dataset = dataset

    def updateData(self, dataset):
        """
        UpdateData sets the dataset variable to the parameter value.
        :param dataset:
        :return: null
        """
        self.dataset = dataset
    def getDataset(self):
        """
        getDataset returns the dataset held by the plotter.
        :return: the dataset variable held by the plotter.
        """
        return self.dataset

    def createXPointPlot(self, point):
        """
        CreateXPointPlot accepts a point as a parameter and plots a
        cyclic voltammogram using voltage as the X-axis variable and
        Current (Im) as the Y-axis variable.

        Called from the core class.

        :param point: integer value [0,MAX_CYCLE_NUMBER=~120] specifying cycle to use to find the current
        :return: null
        """
        f = Figure()
        a = f.add_subplot(111)

        x = self.dataset.getYUnits()
        y = self.dataset.getVerticalAt(point)
        a.set_xlabel("Voltage (V)")
        a.set_ylabel("Current (Im)")
        a.plot(x, y)

        return f

    def createYPointPlot(self, point):
        """
        CreateYPointPlot accepts a point as a parameter and plots a
        line graph of current vs cycle with current as the X-axis
        variable and cycle number as the Y-axis variable.

        Called from the core class.

        :param point: integer value [0,MAX_CYCLE_NUMBER=1600] specifying the point to query in each cycle
        :return: null
        """

        f = Figure()
        a = f.add_subplot(111)

        x = np.array(self.dataset.getXUnits())
        y = np.array(self.dataset.getHorizontalAt(point))

        a.set_xlabel("Cycle")
        a.set_ylabel("Current at point %s (Im)" % (point))

        a.plot(x, y)

        return f

    def createSpectra(self, xHighlight=None, yHighlight=None, contour=False):
        """
        Creates a spectragram graph. This function is called from the
        Core class. The spectragram is a three dimensional plot that
        shows current vs cycle vs time.

        :param xHighlight: defaults to none
        :param yHighlight: defaults to none
        :param contour: defaults to false
        :return: null
        """

        f = Figure()
        a = f.add_subplot(111)

        x = np.array(list(self.dataset.getXUnits()))
        y = np.array(range(len(self.dataset.getYUnits())))


        X, Y = np.meshgrid(x, y)
        Z = np.array(self.dataset.getPlane()).transpose()

        a.pcolormesh(X, Y, Z)
        bar = matplotlib.cm.ScalarMappable()
        bar.set_array(Z)
        if contour:
            a.contour(X, Y, Z)
        f.colorbar(bar, ax=a)

        if xHighlight != None:
            a.axvline(x=xHighlight)
            print("Trying to put bar at " + str(xHighlight))

        if yHighlight != None:
            a.axhline(y=yHighlight)
            print("Trying to put hLine at " + str(yHighlight))

        a.axis([X.min(), X.max(), Y.min(), Y.max()])
        return f



