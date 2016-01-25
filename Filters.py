from Dataset import Dataset
from Utils import Calculations
from scipy.ndimage.filters import gaussian_filter1d, gaussian_filter

# TODO: Add support for RMS bg subtraction

class Filter(Dataset):

    def __init__(self, dataset):
        self.dataset = dataset
        self.plane = None
        self.xPoint = {}
        self.yPoint = {}

    def removeFilter(self):
        return self.dataset

    def addFilter(self, filter):
        filter.dataset = self.dataset
        self.dataset = filter

    def getHorizontalAt(self, point):
        return self.dataset.getHorizontalAt(point)

    def getVerticalAt(self, point):
        return self.dataset.getVerticalAt(point)

    def getPlane(self):
        return self.dataset.getPlane()

    def getYUnits(self):
        return self.dataset.getYUnits()

    def getXUnits(self):
        return self.dataset.getXUnits()

class MinMaxAvgSubtraction(Filter):
    def getHorizontalAt(self, point):
        if not point in self.yPoint.keys():
            data = super().getHorizontalAt(point)
            bg = Calculations.findBackgroundByMinMax(self.dataset)
            self.yPoint[point] = list(map(lambda x: x-bg[point], data))
        return self.yPoint[point]

    def getVerticalAt(self, point):
        if not point in self.xPoint.keys():
            data = super().getVerticalAt(point)
            bg = Calculations.findBackgroundByMinMax(self.dataset)
            self.xPoint[point] = [data[i] - bg[i] for i in range(len(data))]
        return self.xPoint[point]

    def getPlane(self):
        if self.plane == None:
            self.plane = [self.getVerticalAt(i) for i in range(len(self.dataset.getXUnits()))]
        return self.plane


class GaussSmooth(Filter):
    def __init__(self, dataset, sigma=10):
        super().__init__(dataset)
        self.sigma = sigma
    def getHorizontalAt(self, point):
        if not point in self.yPoint.keys():
            self.yPoint[point] = gaussian_filter1d(super().getHorizontalAt(point), self.sigma)
        return self.yPoint[point]

    def getVerticalAt(self, point):
        if not point in self.xPoint.keys():
            self.xPoint[point] = gaussian_filter1d(super().getVerticalAt(point), self.sigma)
        return self.xPoint[point]

    def getPlane(self):
        if self.plane == None:
            self.plane = gaussian_filter(super().getPlane(), self.sigma)
        return self.plane


class BackgroundSubtraction(Filter):

    def getHorizontalAt(self, point):
        if not point in self.yPoint.keys():
            data = super().getHorizontalAt(point)
            bg = Calculations.findBackgroundByAverage(self.dataset)
            self.yPoint[point] = list(map(lambda x: x-bg[point], data))
        return self.yPoint[point]

    def getVerticalAt(self, point):
        if not point in self.xPoint.keys():
            data = super().getVerticalAt(point)
            bg = Calculations.findBackgroundByAverage(self.dataset)
            self.xPoint[point] = [data[i] - bg[i] for i in range(len(data))]
        return  self.xPoint[point]

    def getPlane(self):
        if self.plane == None:
            self.plane = [self.getVerticalAt(i) for i in range(len(self.dataset.getXUnits()))]
        return self.plane


