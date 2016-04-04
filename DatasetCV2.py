
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

    def __init__(self, files, info):
        """

        @param directory:
        @return
        """
        self.info = info
        self.data = list(map(lambda x: CycleCV2.CycleCV2(x), files))

    def getHorizontalAt(self, point):
        """
        Gets the horizontal at a point by querying each cycle in data
        @param point:
        @return
        """
        return list(map(lambda x: x.getDataAtPoint(point), self.data))

    def getVerticalAt(self, point):
        """
        Gets the vertical at a point by querying a single cycle to return all (IM) data contained by that cycle.

        @param point:
        @return null
        """
        return self.data[point].getAllData()

    def getPlane(self):
        """
        Returns a two-dimensional plane by querying each cycle in data to return all (IM) data contained by that cycle.

        @return
        """
        return list(map(lambda x: x.getAllData(), self.data))

    def getYUnits(self):
        """

        @return
        """
        return self.data[0].getVoltages()

    def getXUnits(self):
        """
        @return
        """
        return range(0, len(self.data))

    def __str__(self, *args, **kwargs):
        return "t%s @ %s" % (self.info["Trial"], self.info["Concentration"])



