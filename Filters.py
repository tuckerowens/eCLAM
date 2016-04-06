
######################################################################
## Imports
######################################################################

from Dataset import Dataset
from Utils import Calculations
from scipy.ndimage.filters import gaussian_filter1d, gaussian_filter
import numpy as np, time

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

        @param dataset:
        @return
        """
        self.dataset = dataset
        self.plane = None
        self.xPoint = {}
        self.yPoint = {}

    def removeFilter(self):
        """

        @return
        """
        return self.dataset

    def addFilter(self, filter):
        """

        @param filter:
        @return
        """
        filter.dataset = self.dataset
        self.dataset = filter

    def getHorizontalAt(self, point):
        """
        Overrides dataset.getHorizontalAt
        @param point:
        @return
        """
        return self.dataset.getHorizontalAt(point)

    def getVerticalAt(self, point):
        """
        Overrides dataset.getVerticalAt
        @param point:
        @return
        """
        return self.dataset.getVerticalAt(point)

    def getPlane(self):
        """
        Overrides dataset.getPlane
        @return
        """
        return self.dataset.getPlane()

    def getYUnits(self):
        """
        Overrides dataset.getYUnits
        @return
        """
        return self.dataset.getYUnits()

    def getXUnits(self):
        """
        Overrides dataset.getXUnits
        @return
        """
        return self.dataset.getXUnits()

    def setCurrentIndex(self, index):
        """

        :param index:
        :return:
        """
        self.dataset.setCurrentIndex(index)

    def getCurrentIndex(self):
        return self.dataset.getCurrentIndex()

    def __str__(self, *args, **kwargs):
        return str(self.dataset)



######################################################################
## GaussSmooth
######################################################################

class GaussSmooth(Filter):
    """

    """
    def __init__(self, dataset, sigma=10):
        """
        Constructor

        @param dataset:
        @param sigma:
        @return
        """
        super().__init__(dataset)
        self.sigma = sigma
        
    def getHorizontalAt(self, point):
        """
        Overrides filter.getHorizontalAt

        @param point:
        @return
        """
        if not point in self.yPoint.keys():
            self.yPoint[point] = gaussian_filter1d(super().getHorizontalAt(point), self.sigma)
        return self.yPoint[point]

    def getVerticalAt(self, point):
        """
        Overrides filter.getVerticalAt

        @param point:
        @return
        """
        if not point in self.xPoint.keys():
            self.xPoint[point] = gaussian_filter1d(super().getVerticalAt(point), self.sigma)
        return self.xPoint[point]

    def getPlane(self):
        """
        Overrides filter.getPlane

        @return
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

        @param point:
        @return
        """
        if not point in self.yPoint.keys():
            data = super().getHorizontalAt(point)
            bg = Calculations.findBackgroundByAverage(self.dataset)
            self.yPoint[point] = list(map(lambda x: x-bg[point], data))
        return self.yPoint[point]

    def getVerticalAt(self, point):
        """
        Overrides filter.getVertical

        @param point:
        @return
        """
        if not point in self.xPoint.keys():
            data = super().getVerticalAt(point)
            if not 'bg' in vars(self):
                self.bg = Calculations.findBackgroundByAverage(self.dataset)
            self.xPoint[point] = [data[i] - self.bg[i] for i in range(len(data))]
        return  self.xPoint[point]

    def getPlane(self):
        """
        Overrides filter.getPlane

        @return
        """
        if self.plane == None:
            print("Building Background Substarction")
            start = time.time()
            self.plane = [self.getVerticalAt(i) for i in range(len(self.dataset.getXUnits()))]
            print("Build time: %fs" % (time.time() - start))
        return self.plane

class SNR_Evaluation(Filter):
    def __init__(self, dataset):
        print("Building Local SNR Evalutaion")
        start = time.time()
        super().__init__(RMS_Evaluation(dataset))
        print("\tRMS Evale: %f" % (time.time() - start))
        self.data = [max(self.dataset.getHorizontalAt(i))/min(self.dataset.getHorizontalAt(i)) for i in range(len(self.dataset.getVerticalAt(0)))]
        print("\tData Build: %f" % (time.time() - start))

    def getHorizontalAt(self, point):
        return self.data

    def getVerticalAt(self, point):
        return self.data

    def getPlane(self):
        return [self.data for i in range(len(self.data))]

    def getXUnits(self):
        return np.array(range(len(self.getHorizontalAt(0))))

    def getYUnits(self):
        return np.array(range(len(self.getVerticalAt(0))))

class RMS_Evaluation(Filter):

    def __init__(self, dataset):
        start = time.time()
        super().__init__(dataset)
        print("Building RMS Eval -- ")
        rang = range(len(self.dataset.getVerticalAt(0)))
        self.data = np.array([Calculations.getRMSFromY(self.dataset, i) for i in rang]).transpose()
        print("RMS_Evaluation build in %f" % (time.time() - start))

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return np.array(range(len(self.getHorizontalAt(0))))

class LocalSNR_Evaluation(Filter):

    def __init__(self, dataset):
        start = time.time()
        print("Building Local SNR Evalutaion")
        super().__init__(RMS_Evaluation(dataset))
        print("\tRMS_Evaluation %f" % (time.time() - start))
        maxes = [max(self.dataset.getHorizontalAt(i)) for i in range(len(self.dataset.getVerticalAt(0)))]
        print("\tMaxes found %f" % (time.time() - start))
        self.data = [[self.dataset.getVerticalAt(j)[i]/maxes[i] for i in range(len(self.dataset.getVerticalAt(j)))] for j in range(len(self.dataset.getHorizontalAt(0)))]
        print("\tdata generated %f" % (time.time() - start))
        print ("---")

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return np.array(range(len(self.data)))

