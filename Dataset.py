
######################################################################
## Dataset
######################################################################
import time
class Dataset:
    """
    Dataset is an interface that provides several methods that subclasses need to implement.

    The reason that an interface is used is so that we can specify different datasets for different types of testing.
    """

    def __init__(self):
        self.min = None
        self.max = None
        self.gMinCoord = None
        self.gMaxCoord = None

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
        if self.gMaxCoord == None:
            m = self.getMax()
            self.gMaxCoord = self.getCoordsOfValue(m)
        return self.gMaxCoord


    def getCoordsOfValue(self, m):
        start = time.time()
        plane = self.getPlane()
        cols = [x for x in range(len(self.getHorizontalAt(0))) if x in plane[x]]
        print("\tcols : %fs" % (time.time() - start))
        rows = [x for sublist in [list(filter(lambda x: l[x] == m, range(len(l)))) for l in self.getPlane()] for x in sublist]
        print("\trows : %fs" % (time.time() - start))
        matches = zip(cols, rows)
        self.gMaxCoord = list(matches)
        print("Get %f Coord Gen : %fs" % (m, time.time() - start))

    def getMinCoord(self):
        if self.gMinCoord == None:
            m = self.getMax()
            self.gMinCoord = self.getCoordsOfValue(m)
        return self.gMinCoord


    def getMin(self):
        if self.min == None:
            start = time.time()
            self.min =  min([min(i) for i in self.getPlane()])
            print("Found Min in %f" % (time.time() - start))

        return self.min

    def getMax(self):
        if self.max == None:
            start = time.time()
            self.max = max([max(i) for i in self.getPlane()])
            print("Found Max in %f" % (time.time() - start))
        return self.max


    def getInfo(self):
        """
        This function is used to return useful info
        to the caller which in most cases the plotter.
        It's this information that eventually appears in the
        plot info text box
        :return: string of information, well formatted
        """

        outstr = str(self) + '\n'
        outstr += "  Min of %f @ %s" % (self.getMin(), str(self.getMinCoord())) + '\n'
        outstr += "  Max of %f @ %s" % (self.getMax(), str(self.getMaxCoord()))
        return outstr