
######################################################################
## Imports
######################################################################

import numpy as np, time
from Dataset import Dataset
import math

# TODO: Add Support for RMS

######################################################################
## Calculations
######################################################################

def findBackgroundByAverage(dataset: Dataset, startPoint=0, endPoint=5):
    bg = []
    for i in range(len(dataset.getYUnits())):
        bg.append(sum(dataset.getHorizontalAt(i)[startPoint:endPoint]) / (endPoint-startPoint))
    return bg

def findBackgroundByMinMax(dataset: Dataset):
    bg = []
    for i in range(len(dataset.getYUnits())):
        bg.append(abs(min(dataset.getHorizontalAt( i)) + max(dataset.getHorizontalAt(i)) / 2.0))
    return bg

def getXFromMinImAtY(dataset: Dataset, point):
    return list(dataset.getHorizontalAt(point)).index(min(dataset.getHorizontalAt( point)))

def getXFromMaxImAtY(dataset: Dataset, point):
    return list(dataset.getHorizontalAt(point)).index(max(dataset.getHorizontalAt( point)))


def getYFromMinImAtX(dataset: Dataset, point):
    return list(dataset.getVerticalAt(point)).index(min(dataset.getVerticalAt( point)))

def getYFromMaxImAtX(dataset: Dataset, point):
    return list(dataset.getVerticalAt(point)).index(max(dataset.getVerticalAt( point)))


def getRMSFromY(dataset: Dataset, point: int, width=5):
    data = dataset.getHorizontalAt(point)
    out =  [math.sqrt(sum(map(lambda x: x**2, data[i:i+width]))/width) for i in range(len(data)-width)]
    return out



def getXAtMinIm(dataset: Dataset):
    data = dataset.getPlane()
    curMin = data[0][0]
    bestCycle = 0
    for cycle in range(len(data)):
        if min(data[cycle]) < curMin:
            curMin = min(data[cycle])
            bestCycle = cycle
    return bestCycle

def getXAtMaxIm(dataset: Dataset):
    data = dataset.getPlane()
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
