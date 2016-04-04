
######################################################################
## Dataset
######################################################################

class Dataset:
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
