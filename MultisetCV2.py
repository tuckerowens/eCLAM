
######################################################################
## Imports
######################################################################

import Dataset

######################################################################
## Multiset
######################################################################

class MultisetCV2(Dataset.Dataset):
    """
    DatasetCV2 is a subclass of the dataset class and overrides all of the methods it contains.
    @field data: Data is a list of cycles found in the specified directory
    """

    def __init__(self):
        """
        @param directory
        @return
        """
        self.data = []
        self.datasets = []

    def addDataset(self, dataset):
        self.datasets.append(dataset)

    def getSize(self):
        """

        @return size of list of datasets
        """
        print("Multiset getsize: ", self.datasets.__len__())
        return self.datasets.__len__()

    def getHorizontalAt(self, option, point):
        """
        Gets the horizontal at a point by querying each cycle in data
        @param option if positive number then return dataset at index=option, else, return average of all
        @param point:
        @return
        """

        # added this to compute average if option was negative
        # abs(option) is the number of datasets in the multi-set

        # right now the calling class defaults to calling the average
        # so if you have multiple files, there is currently no way
        # to specify a single set to look at. This can be changed
        # by adding an additional button to the gui

        print("option:", option)
        if option < 0:
            print("plotting average")
            ave_point = []
            for i in range(0, len(self.datasets[0].data)):
                ave_point.append(0)
                for j in range(0, abs(option)):
                    ave_point[i] += self.datasets[j].data[i].getDataAtPoint(point)
                ave_point[i] /= abs(option)
            return ave_point

        return list(map(lambda x: x.getDataAtPoint(point), self.datasets[0].data))

    def getVerticalAt(self, option, point):
        """
        Gets the vertical at a point by querying a single cycle to return all (IM) data contained by that cycle.
        @param option if positive number then return dataset at index=option, else, return average of all
        @param point:
        @return null
        """
        return self.datasets[option].data[point].getAllData()

    def getPlane(self, option):
        """
        Returns a two-dimensional plane by querying each cycle in data to return all (IM) data contained by that cycle.
        @param option if positive number then return dataset at index=option, else, return average of all
        @return
        """
        return list(map(lambda x: x.getAllData(), self.datasets[option].data))

    def getYUnits(self, option):
        """

        @param option if positive number then return dataset at index=option, else, return average of all
        @return
        """


        return self.datasets[option].data[option].getVoltages()

    def getXUnits(self, option):
        """

        @param option if positive number then return dataset at index=option, else, return average of all
        @return
        """
        return range(0, len(self.datasets[abs(option)].data))
