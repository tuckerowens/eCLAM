
######################################################################
## Imports
######################################################################

from Dataset import Dataset
from Utils import Calculations
from scipy.ndimage.filters import gaussian_filter1d, gaussian_filter
import numpy as np, time
from FlowFinder import FlowFinder
import subprocess
# TODO: Add support for RMS bg subtraction
import Utils.AskUserBox as ub
######################################################################
## Filter
######################################################################
from Utils.AskUserBox import AskUser


class Filter(Dataset):

    takesMultiset = False
    filterSet = []

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


class RollingAverage(Filter):
    def __init__(self, dataset):
        super().__init__(dataset)
        res = AskUser(["Rolling Average Width: "], defaults=[3])
        width = int(res[0])
        self.data = [Calculations.findBackgroundByAverage(self.dataset, startPoint=sp, endPoint=(sp+width)) for sp in range(len(dataset.getHorizontalAt(0))-width)]

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return np.array(range(len(self.getHorizontalAt(0))))

    def __str__(self, *args, **kwargs):
        return "RollingAvg(" + str(self.dataset) + ")"


######################################################################
## GaussSmooth
######################################################################

class GaussSmooth(Filter):
    """

    """
    def __init__(self, dataset):
        """
        Constructor

        @param dataset:
        @param sigma:
        @return
        """
        super().__init__(dataset)
        self.logY = dataset.logY
        self.sigma = AskUser(["Gauss Smooth Sigma: "], defaults=[10])
        
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

    def __str__(self, *args, **kwargs):
        return "Gauss(" + str(self.dataset) + ")"


######################################################################
## BackgroundSubtraction
######################################################################

class BackgroundSubtraction(Filter):
    """

    """

    def __init__(self, dataset, start=None, width=None):
        super().__init__(dataset)
        if start != None and width != None:
            info = [start, width]
        else:
            info = AskUser(["Background Starting Cycle: ", "Background Width: "], defaults=[0, 5])
        self.logY = dataset.logY
        bg = np.array(Calculations.findBackgroundByAverage(self.dataset, startPoint=int(info[0]), endPoint=(int(info[1])-int(info[0]))))
        inner = np.array(dataset.getPlane())
        self.data = [i - bg for i in inner]


    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        """
        Overrides filter.getPlane

        @return
        """

        return self.data

    def __str__(self, *args, **kwargs):
        return "-BG(" + str(self.dataset) + ")"



class RMS_Evaluation(Filter):

    def __init__(self, dataset):
        super().__init__(dataset)
        rang = range(len(self.dataset.getVerticalAt(0)))
        self.data = np.array([Calculations.getRMSFromY(self.dataset, i) for i in rang]).transpose()

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return np.array(range(len(self.getHorizontalAt(0))))

    def __str__(self, *args, **kwargs):
        return "RMS(" + str(self.dataset) + ")"


class FFT_Eval(Filter):
    logY = True

    def __init__(self, dataset):
        super().__init__(dataset)

        f_ishift = np.fft.ifftshift(np.array(self.dataset.getPlane()))
        img_back = np.fft.ifft2(f_ishift)
        self.data = np.abs(img_back)

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return np.array(range(len(self.data)))

    def __str__(self, *args, **kwargs):
        return "FFT(" + str(self.dataset) + ")"


class Average(Filter):
    takesMultiset = True

    def __init__(self, datasets):
        super().__init__(datasets[0])
        self.name = "Average "
        self.logY = datasets[0].logY
        for d in datasets:
            self.name += str(d) + '|'
        self.datasets = [ds.getPlane() for ds in datasets]

        self.data = np.average(self.datasets, 0)

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        print("get Vert called %i" % (point))
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return self.dataset.getXUnits()

    def getYUnits(self):
        return self.dataset.getYUnits()

    def __str__(self):
        return self.name

class StandardDeviation(Filter):
    takesMultiset = True
    filterSet = [lambda this, data: Average(data), lambda this, data: Average(data).addDataset(this, label="Upper STD"),
                 lambda this, data: Average(data).addDataset(this, scale=-1, label="Lower STD")]

    def __init__(self, datasets):
        super().__init__(datasets[0])
        self.logY = datasets[0].logY
        self.name = "STD "
        for d in datasets:
            self.name += str(d) + '|'
        self.datasets = [ds.getPlane() for ds in datasets]
        self.data = np.std(self.datasets, 0)

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return self.dataset.getXUnits()

    def getYUnits(self):
        return self.dataset.getYUnits()

    def __str__(self):
        return self.name



class OptimalBGSub(Filter):

    def __init__(self, dataset):
        super().__init__(dataset)
        print("Why don't you grab a cup of coffee")
        bestIndex = 0
        res = AskUser(["Scan Width: "], [5])
        width = int(res[0])
        best = -1
        l = len(dataset.getHorizontalAt(0)) - width
        for i in range(len(dataset.getHorizontalAt(0)) - width):
            print(str((i/l)*100) + "% done")
            ds = RMS_Evaluation(BackgroundSubtraction(dataset, start=i, width=width))
            for j in range(len(ds.getVerticalAt(0))):
                h = ds.getHorizontalAt(j)
                snr = max(h)/min(h)
                if best < snr:
                    best = snr
                    bestIndex = i
                    print("Updating best to " + str(bestIndex))

        self.dataset = BackgroundSubtraction(dataset, start=bestIndex, width=width)


class LocalSNR_Evaluation(Filter):

    def __init__(self, dataset):
        super().__init__(RMS_Evaluation(dataset))
        maxes = [min(self.dataset.getHorizontalAt(i)) for i in range(len(self.dataset.getVerticalAt(0)))]
        self.data = [[np.square(self.dataset.getVerticalAt(j)[i]/maxes[i]) for i in range(len(self.dataset.getVerticalAt(j)))] for j in range(len(self.dataset.getHorizontalAt(0)))]

    def getHorizontalAt(self, point):
        return [col[point] for col in self.data]

    def getVerticalAt(self, point):
        return self.data[point]

    def getPlane(self):
        return self.data

    def getXUnits(self):
        return np.array(range(len(self.data)))

    def __str__(self, *args, **kwargs):
        return "SNR(" + str(self.dataset) + ")"

#
# class SNR_Evaluation(Filter):
#     def __init__(self, dataset):
#         super().__init__(RMS_Evaluation(dataset))
#         self.data = [max(self.dataset.getHorizontalAt(i))/min(self.dataset.getHorizontalAt(i)) for i in range(len(self.dataset.getVerticalAt(0)))]
#
#     def getHorizontalAt(self, point):
#         return self.data
#
#     def getVerticalAt(self, point):
#         return self.data
#
#     def getPlane(self):
#         return [self.data for i in range(len(self.data))]
#
#     def getXUnits(self):
#         return np.array(range(len(self.getHorizontalAt(0))))
#
#     def getYUnits(self):
#         return np.array(range(len(self.getVerticalAt(0))))
#
#     def __str__(self, *args, **kwargs):
#         return "SNR(" + str(self.dataset) + ")"
