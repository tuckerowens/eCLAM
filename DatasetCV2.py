import Dataset, os, CycleCV2
import re

class DatasetCV2(Dataset.Dataset):

    def __init__(self, directory):
        files = []
        for file in os.listdir(directory):
            if ".DTA" in file:
                files.append(directory + file)
        files = sorted(files, key=lambda f: int(re.search("(?:#)(.*)(?=\.DTA)", f).group(1)))
        self.data = list(map(lambda x: CycleCV2.CycleCV2(x), files))


    def getHorizontalAt(self, point):
        return list(map(lambda x: x.getDataAtPoint(point), self.data))

    def getVerticalAt(self, point):
        return self.data[point].getAllData()

    def getPlane(self):
        return list(map(lambda x: x.getAllData(), self.data))

    def getYUnits(self):
        return self.data[0].getVoltages()

    def getXUnits(self):
        return range(0, len(self.data))
