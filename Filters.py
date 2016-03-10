
######################################################################
## Imports
######################################################################

from Dataset import Dataset
from Utils import Calculations
from scipy.ndimage.filters import gaussian_filter1d, gaussian_filter

# TODO: Add support for RMS bg subtraction

######################################################################
## Filter
######################################################################

class Filter(Dataset):
    """
    Filter is a class that implements the dataset interface. It
    provides methods for passing the unaltered dataset through a
    filter to create an altered dataset. Such alterations could include
    a dataset with the background subtracted or with a gaussian blur
    applied.

    @field dataset:
    @field plane:
    @field sigma:
    @field xPoint:
    @field yPoint:
    """
    def __init__(self, dataset):
        """
        The Filter constructor initializes the dataset variable
        to the param value, plane to none, and xPoint
        and yPoint to empty lists.

        :param dataset:
        :return:
        """
        self.dataset = dataset
        self.plane = None
        self.xPoint = {}
        self.yPoint = {}

    def removeFilter(self):
        """

        :return:
        """
        return self.dataset

    def addFilter(self, filter):
        """

        :param filter:
        :return:
        """
        filter.dataset = self.dataset
        self.dataset = filter

    def getHorizontalAt(self, point):
        """
        Overrides dataset.getHorizontalAt
        :param point:
        :return:
        """
        return self.dataset.getHorizontalAt(point)

    def getVerticalAt(self, point):
        """
        Overrides dataset.getVerticalAt
        :param point:
        :return:
        """
        return self.dataset.getVerticalAt(point)

    def getPlane(self):
        """
        Overrides dataset.getPlane
        :return:
        """
        return self.dataset.getPlane()

    def getYUnits(self):
        """
        Overrides dataset.getYUnits
        :return:
        """
        return self.dataset.getYUnits()

    def getXUnits(self):
        """
        Overrides dataset.getXUnits
        :return:
        """
        return self.dataset.getXUnits()

######################################################################
## MinMaxAvgSubtraction
######################################################################

class MinMaxAvgSubtraction(Filter):
    """

    """
    def getHorizontalAt(self, point):
        """
        Overrides filter.getHorizontalAt
        :param point:
        :return:
        """
        if not point in self.yPoint.keys():
            data = super().getHorizontalAt(point)
            bg = Calculations.findBackgroundByMinMax(self.dataset)
            self.yPoint[point] = list(map(lambda x: x-bg[point], data))
        return self.yPoint[point]

    def getVerticalAt(self, point):
        """
        Overrides filter.getVerticalAt
        :param point:
        :return:
        """
        if not point in self.xPoint.keys():
            data = super().getVerticalAt(point)
            bg = Calculations.findBackgroundByMinMax(self.dataset)
            self.xPoint[point] = [data[i] - bg[i] for i in range(len(data))]
        return self.xPoint[point]

    def getPlane(self):
        """
        Overrides filter.getPlane
        :return:
        """

        if self.plane == None:
            self.plane = [self.getVerticalAt(i) for i in range(len(self.dataset.getXUnits()))]
        return self.plane

######################################################################
## GaussSmooth
######################################################################

class GaussSmooth(Filter):
    """

    """
    def __init__(self, dataset, sigma=10):
        """
        Constructor

        :param dataset:
        :param sigma:
        :return:
        """
        super().__init__(dataset)
        self.sigma = sigma
    def getHorizontalAt(self, point):
        """
        Overrides filter.getHorizontalAt

        :param point:
        :return:
        """
        if not point in self.yPoint.keys():
            self.yPoint[point] = gaussian_filter1d(super().getHorizontalAt(point), self.sigma)
        return self.yPoint[point]

    def getVerticalAt(self, point):
        """
        Overrides filter.getVerticalAt

        :param point:
        :return:
        """
        if not point in self.xPoint.keys():
            self.xPoint[point] = gaussian_filter1d(super().getVerticalAt(point), self.sigma)
        return self.xPoint[point]

    def getPlane(self):
        """
        Overrides filter.getPlane

        :return:
        """
        if self.plane == None:
            self.plane = gaussian_filter(super().getPlane(), self.sigma)
        return self.plane


######################################################################
## BackgroundSubtraction
######################################################################

class BackgroundSubtraction(Filter):
    """

    """

    def getHorizontalAt(self, point):
        """
        Overrides filter.getHorizontalAt

        :param point:
        :return:
        """
        if not point in self.yPoint.keys():
            data = super().getHorizontalAt(point)
            bg = Calculations.findBackgroundByAverage(self.dataset)
            self.yPoint[point] = list(map(lambda x: x-bg[point], data))
        return self.yPoint[point]

    def getVerticalAt(self, point):
        """
        Overrides filter.getVertical

        :param point:
        :return:
        """
        if not point in self.xPoint.keys():
            data = super().getVerticalAt(point)
            bg = Calculations.findBackgroundByAverage(self.dataset)
            self.xPoint[point] = [data[i] - bg[i] for i in range(len(data))]
        return  self.xPoint[point]

    def getPlane(self):
        """
        Overrides filter.getPlane

        :return:
        """
        if self.plane == None:
            self.plane = [self.getVerticalAt(i) for i in range(len(self.dataset.getXUnits()))]
        return self.plane


