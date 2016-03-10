
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
    This is the class that handles the plotting.
    """

    def __init__(self, dataset):
        """
        Constructor

        :param dataset: The dataset to be plotted
        :return:
        """
        self.dataset = dataset

    def updateData(self, dataset):
        """

        :param dataset:
        :return:
        """
        self.dataset = dataset
    def getDataset(self):
        """

        :return:
        """
        return self.dataset

    def createXPointPlot(self, point):
        """

        :param point:
        :return:
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

        :param point:
        :return:
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

        :param xHighlight:
        :param yHighlight:
        :param contour:
        :return:
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



