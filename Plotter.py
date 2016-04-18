
######################################################################
## Imports
######################################################################

import matplotlib, time
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

        @param dataset: The dataset to be plotted
        @return null
        """
        self.dataset = dataset


    def updateData(self, dataset):
        """
        UpdateData sets the dataset variable to the parameter value.
        @param dataset:
        @return null
        """
        self.dataset = dataset
    def getDataset(self):
        """
        getDataset returns the dataset held by the plotter.
        @return the dataset variable held by the plotter.
        """
        return self.dataset

    def __str__(self, *args, **kwargs):
        if self.plotInfoStr != None:
            return self.plotInfoStr
        return ""


    def createXPointPlot(self, point):
        """
        CreateXPointPlot accepts a point as a parameter and plots a
        cyclic voltammogram using voltage as the X-axis variable and
        Current (Im) as the Y-axis variable.

        Called from the engineV2 class.

        @param point: integer value [0,MAX_CYCLE_NUMBER=~120] specifying cycle to use to find the current
        @return null
        """

        # changed this to now plot each table located in the dataset side by side
        # will add function later to display a more accurate legend
        f = Figure()
        a = f.add_subplot(111)
        tmp_index = self.dataset.getCurrentIndex()
        legend = []
        self.plotInfoStr = ""
        for i in range(0, self.dataset.getSize()):
            self.plotInfoStr += self.dataset.getInfo() + '\n'
            legend.append(str(self.dataset))
            x = self.dataset.getYUnits()
            y = self.dataset.getVerticalAt(point)
            a.set_xlabel("Voltage (V)")
            a.set_ylabel("Current (Im)")
            if self.dataset.logifyY:
                a.semilogy(x, np.abs(y))
            else:
                a.plot(x, y)

            self.dataset.setCurrentIndex((self.dataset.getCurrentIndex() + 1) % self.dataset.getSize())
        a.legend(legend, loc='upper left')  # change this later to reflect cycle numbers or something relevant
        self.dataset.setCurrentIndex(tmp_index)
        f.suptitle(str(self.dataset))
        return f

    def createYPointPlot(self, point):
        """
        CreateYPointPlot accepts a point as a parameter and plots a
        line graph of current vs cycle with current as the X-axis
        variable and cycle number as the Y-axis variable.

        Called from the engineV2 class.

        @param point: integer value [0,MAX_CYCLE_NUMBER=1600] specifying the point to query in each cycle
        @return null
        """


        f = Figure()
        a = f.add_subplot(111)

        tmp_index = self.dataset.getCurrentIndex()
        legend = []
        self.plotInfoStr = ""
        for i in range(0, self.dataset.getSize()):
            print("Plotting index ", i )
            legend.append(str(self.dataset))
            self.plotInfoStr += self.dataset.getInfo() + '\n'
            x = np.array(self.dataset.getXUnits())
            y = np.array(self.dataset.getHorizontalAt(point))
            a.set_xlabel("Voltage (V)")
            a.set_ylabel("Current (Im)")
            if self.dataset.logifyY:
                a.semilogy(x, np.abs(y))
            else:
                a.plot(x, y)

            self.dataset.setCurrentIndex((self.dataset.getCurrentIndex() + 1) % self.dataset.getSize())
        a.legend(legend, loc='upper left')  # change this later to reflect cycle numbers or something relevant
        self.dataset.setCurrentIndex(tmp_index)
        f.suptitle(str(self.dataset))
        a.set_xlabel("Cycle")
        a.set_ylabel("Current at point %s (Im)" % point)



        return f

    def createSpectra(self, xHighlight=None, yHighlight=None, contour=False, index=0):
        """
        Creates a spectragram graph. This function is called from the
        Core class. The spectragram is a three dimensional plot that
        shows current vs cycle vs time.

        @param xHighlight: defaults to none
        @param yHighlight: defaults to none
        @param contour: defaults to false
        @return null
        """

        # haven't touched this yet. will likely add new field in gui to cycle through indexes of spectras

        self.plotInfoStr = self.dataset.getInfo()

        print("Plotting spectra at index:", index)
        f = Figure()
        a = f.add_subplot(111)

        x = np.array(list(self.dataset.getXUnits()))
        y = np.array(range(len(self.dataset.getYUnits())))

        print("---\nsize of x: %i\nsize of y: %i" % (len(x), len(y)))

        X, Y = np.meshgrid(x, y)
        Z = np.array(self.dataset.getPlane()).transpose()

        if (self.dataset.logifyY):
            Z = Z + np.abs(Z.min())
            a.pcolormesh(X, Y, Z, norm=matplotlib.colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
        else:
            a.pcolormesh(X, Y, Z)
        bar = matplotlib.cm.ScalarMappable()
        bar.set_array(Z)
        if contour:
            a.contour(X, Y, Z)
        f.colorbar(bar, ax=a, label="Current (Im)")
        f.suptitle(str(self.dataset))

        if xHighlight != None:
            a.axvline(x=xHighlight)
            print("Trying to put bar at " + str(xHighlight))

        if yHighlight != None:
            a.axhline(y=yHighlight)
            print("Trying to put hLine at " + str(yHighlight))

        a.axis([X.min(), X.max(), Y.min(), Y.max()])
        return f
