
######################################################################
## Imports
######################################################################

import Dataset, os, CycleCV2
import re

######################################################################
## DatasetCV2
######################################################################

class DatasetCV2(Dataset.Dataset):
    """
    DatasetCV2 is a subclass of the dataset class and overrides all of the methods it contains.
    @field data: Data is a list of cycles found in the specified directory
    """

    def __init__(self, directory):
        """

        @param directory:
        @return
        """
        print("Creating dataset from dir: ", directory)
        files = []
        for file in os.listdir(directory):
            if ".DTA" in file:
                files.append(directory + file)
        files = sorted(files, key=lambda f: int(re.search("(?:#)(.*)(?=\.DTA)", f).group(1)))
        self.data = list(map(lambda x: CycleCV2.CycleCV2(x), files))


    def getHorizontalAt(self, option, point):
        """
        Gets the horizontal at a point by querying each cycle in data

        @param option does nothing in datasetCV2
        @param point:
        @return
        """
        return list(map(lambda x: x.getDataAtPoint(point), self.data))

    def getVerticalAt(self, option, point):
        """
        Gets the vertical at a point by querying a single cycle to return all (IM) data contained by that cycle.

        @param option does nothing in datasetCV2
        @param point:
        @return null
        """
        return self.data[point].getAllData()

    def getPlane(self, option):
        """
        Returns a two-dimensional plane by querying each cycle in data to return all (IM) data contained by that cycle.

        @param option does nothing in datasetCV2
        @return
        """
        return list(map(lambda x: x.getAllData(), self.data))

    def getYUnits(self, option):
        """

        @param option does nothing in datasetCV2
        @return
        """
        return self.data[0].getVoltages()

    def getXUnits(self, option):
        """

        @param option does nothing in datasetCV2
        @return
        """
        return range(0, len(self.data))

