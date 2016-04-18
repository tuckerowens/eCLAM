
######################################################################
## Dataset
######################################################################
import time
import numpy as np
class Dataset:
    logY = False
    """
    Dataset is an interface that provides several methods that subclasses need to implement.

    The reason that an interface is used is so that we can specify different datasets for different types of testing.
    """


    def getSize(self):
        """

        @return size 1
        """
        return 1

    def getIndex(self, index):
        """

        :param index:
        :return:
        """
        return self


    def getHorizontalAt(self, point):
        """
        @param point
        @return
        """
        return NotImplemented

    def getVerticalAt(self, point):
        """
        @param option does nothing in dataset
        @param point
        @return
        """
        return NotImplemented

    def getPlane(self):
        """

        @param option does nothing in dataset
        @return
        """
        return  NotImplemented

    def getYUnits(self):
        """

        @param option does nothing in dataset
        @return
        """
        return NotImplemented

    def getXUnits(self):
        """

        @param option does nothing in dataset
        @return
        """
        return NotImplemented

    def setCurrentIndex(self, index):
        """

        :param index:
        :return:
        """
        self.currentIndex = 0

    def getCurrentIndex(self):
        return self.currentIndex

    def setAverageDataset(self, enable):
        pass

    def getMaxCoord(self):
        if not 'gMaxCoord' in vars(self):
            m = self.getMax()
            self.gMaxCoord = self.getCoordsOfValue(m)[0]
        return self.gMaxCoord


    def getCoordsOfValue(self, m):
        start = time.time()
        plane = self.getPlane()
        cols = [x for x in range(len(self.getHorizontalAt(0))) if m in plane[x]]
        rows = [x for sublist in [list(filter(lambda x: l[x] == m, range(len(l)))) for l in self.getPlane()] for x in sublist]
        matches = zip(cols, rows)
        return (list(matches))

    def getMinCoord(self):
        if not 'gMinCoord' in vars(self):
            m = self.getMin()
            self.gMinCoord = self.getCoordsOfValue(m)[0]
        return self.gMinCoord


    def getMin(self):
        if not 'min' in vars(self):
            self.min =  min([min(i) for i in self.getPlane()])

        return self.min

    def getMax(self):
        if not 'max' in vars(self):
            self.max = max(np.array(self.getPlane()).flatten())
        return self.max


    def addDataset(self, dataset, scale=1, label=""):
        source = np.array(self.getPlane())
        return SimpleDataset(source + (np.array(dataset.getPlane()) * scale), self.getXUnits(), self.getYUnits(), label=label)


    def getInfo(self):
        """
        This function is used to return useful info
        to the caller which in most cases the plotter.
        It's this information that eventually appears in the
        plot info text box
        :return: string of information, well formatted
        """

        outstr = str(self) + '\n'
        outstr += "  Min %s @ %s" % (str(self.getMin()), str(self.getMinCoord())) + '\n'
        outstr += "  Max %s @ %s" % (str(self.getMax()), str(self.getMaxCoord()))
        return outstr


class SimpleDataset(Dataset):
    def __init__(self, data, xInfo, yInfo, label="Simple Dataset"):
        self.data = data
        self.xInfo = xInfo
        self.yInfo = yInfo
        self.label = label

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return self.xInfo

    def getYUnits(self):
        return self.yInfo

    def __str__(self):
        return self.label