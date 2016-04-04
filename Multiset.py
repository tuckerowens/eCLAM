import Dataset, AverageDataset

######################################################################
## Multiset
######################################################################

class Multiset(Dataset.Dataset):
    """
    Dataset is an interface that provides several methods that subclasses need to implement.

    The reason that an interface is used is so that we can specify different datasets for different types of testing.
    """
    def __init__(self):
        self.datasets = []
        self.average = ""
        self.currentIndex = 0
        self.currentDataset = ""

    def is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def addDataset(self, dataset):
        self.datasets.append(dataset)

        if self.average == "":
            self.average = AverageDataset.AverageDataset(len(dataset.data), len(dataset.data[0].table), len(dataset.data[0].table[0]))

        if self.currentDataset == "":
            self.currentDataset = self.datasets[self.getSize() - 1]

        for c in range(0, len(self.datasets[0].data)):
            for x in range(0, len(self.datasets[0].data[self.getSize() - 1].table)):
                for y in range(0, len(self.datasets[0].data[self.getSize() - 1].table[0])):
                    if self.is_float(str=dataset.data[c].table[x][y]):
                        addend_a = float(self.average.data[c].table[x][y]) * (self.getSize() - 1) / self.getSize()
                        addend_b = float(dataset.data[c].table[x][y]) / self.getSize()
                        self.average.data[c].table[x][y] = addend_a + addend_b
                    else:
                        self.average.data[c].table[x][y] = dataset.data[c].table[x][y]

    def getSize(self):
        """
        :return:
        """
        return len(self.datasets)

    def getHorizontalAt(self, point):
        """
        :param point:
        :return:
        """
        return self.currentDataset.getHorizontalAt(point)

    def getVerticalAt(self, point):
        """
        :param point:
        :return:
        """
        return self.currentDataset.getVerticalAt(point)

    def getPlane(self):
        """

        :return:
        """
        return self.currentDataset.getPlane()

    def getYUnits(self):
        """

        :return:
        """
        return self.currentDataset.getYUnits()

    def getXUnits(self):
        """

        :return:
        """
        return self.currentDataset.getXUnits()

    def setCurrentIndex(self, index):
        """

        :param index:
        :return:
        """
        self.currentIndex = index

    def getCurrentIndex(self):
        return self.currentIndex

    def setAverageDataset(self, enable):
        if enable == True:
            self.currentDataset = self.average
        else:
            self.currentDataset = self.datasets[self.currentIndex]
