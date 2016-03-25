
######################################################################
## Imports
######################################################################

import numpy as np
from Dataset import Dataset

# TODO: Add Support for RMS

######################################################################
## Calculations
######################################################################

def findBackgroundByAverage(dataset: Dataset, startPoint=0, endPoint=5):
    bg = []
    for i in range(len(dataset.getYUnits(0))):
        bg.append(sum(dataset.getHorizontalAt(0, i)[startPoint:endPoint]) / (endPoint-startPoint))
    return bg

def findBackgroundByMinMax(dataset: Dataset):
    bg = []
    for i in range(len(dataset.getYUnits(0))):
        bg.append(abs(min(dataset.getHorizontalAt(0, i)) + max(dataset.getHorizontalAt(0, i)) / 2.0))
    return bg

def getXFromMinImAtY(dataset: Dataset, point):
    return list(dataset.getHorizontalAt(0, point)).index(min(dataset.getHorizontalAt(0, point)))

def getXFromMaxImAtY(dataset: Dataset, point):
    return list(dataset.getHorizontalAt(0, point)).index(max(dataset.getHorizontalAt(0, point)))


def getYFromMinImAtX(dataset: Dataset, point):
    return list(dataset.getVerticalAt(0, point)).index(min(dataset.getVerticalAt(0, point)))

def getYFromMaxImAtX(dataset: Dataset, point):
    return list(dataset.getVerticalAt(0, point)).index(max(dataset.getVerticalAt(0, point)))


def getXAtMinIm(dataset: Dataset):
    data = dataset.getPlane(0)
    curMin = data[0][0]
    bestCycle = 0
    for cycle in range(len(data)):
        if min(data[cycle]) < curMin:
            curMin = min(data[cycle])
            bestCycle = cycle
    return bestCycle

def getXAtMaxIm(dataset: Dataset):
    data = dataset.getPlane(0)
    curMin = data[0][0]
    bestCycle = 0
    for cycle in range(len(data)):
        if max(data[cycle]) > curMin:
            curMin = max(data[cycle])
            bestCycle = cycle
    return bestCycle

def getYAtMaxIm(dataset: Dataset):
    return getYFromMaxImAtX(dataset, getXAtMaxIm(dataset))

def getYAtMinIm(dataset: Dataset):
    return getYFromMinImAtX(dataset, getXAtMinIm(dataset))
