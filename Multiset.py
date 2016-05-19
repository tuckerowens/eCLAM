import Dataset, AverageDataset, time, concurrent.futures as futures

######################################################################
# Multiset
######################################################################

class Multiset(Dataset.Dataset):

    fillPlot = False
    """
    Dataset is an interface that provides several methods that subclasses need to implement.

    The reason that an interface is used is so that we can specify different datasets for different types of testing.
    """
    def __init__(self):
        super().__init__()
        self.datasets = []
        self.average = ""
        self.currentIndex = 0
        self.currentDataset = ""
        self.logifyY = False

    def is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def addDataset(self, dataset):

        self.datasets.append(dataset)
        self.logifyY = self.logifyY or dataset.logY

        # initialize the currentDataset pointer a dataset
        if self.currentDataset == "":
            self.currentDataset = self.datasets[self.getSize() - 1]


    def getSize(self):
        """
        :return:
        """
        if self.currentDataset == self.average:
            return 1
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
        self.currentDataset = self.datasets[index]

    def getCurrentIndex(self):
        return self.currentIndex

    def setAverageDataset(self, enable):
        print("Enable average:", enable)
        self.fillPlot = enable

    def applyFilter(self, filter: Dataset):
        output = Multiset()
        if filter.takesMultiset:
            if filter.filterSet != []:
                for f in filter.filterSet:
                    output.addDataset(f(filter(self.datasets), self.datasets))
                return output
            output.addDataset(filter(self.datasets))
            return output


        for ds in self.datasets:
            output.addDataset(filter(ds))
        return output

    def __str__(self, *args, **kwargs):
        return str(self.currentDataset)


