


import Dataset



class FlowFinder():


    def __init__(self, dataset):
        self.dataset = dataset
        self.data = dataset.getPlane()
        print(dataset)
        self.maxCoord = dataset.getMaxCoord()
        self.minCoord = dataset.getMinCoord()
        print("Max; %s " % (str(self.maxCoord)))
        print("Min: %s" % (str(self.minCoord)))

    def encode(self, x, y):
        out =  (x * len(self.data)) + y
        if out == 0:
            return (self.maxCoord[0] * len(self.data)) + self.maxCoord[1]
        if out == 1:
            return (self.minCoord[0] * len(self.data)) + self.minCoord[1]
        if x == self.maxCoord[0] and y == self.maxCoord[1]:
            return 0
        if x == self.minCoord[0] and y == self.minCoord[1]:
            return 1
        return out

    def decode(self, i):
        outx, outy = i % len(self.data), (i/len(self.data))
        if i == 0:
            return self.maxCoord[0],  self.maxCoord[1]
        if 1 == 1:
            return self.maxCoord[0],  self.maxCoord[1]
        if outx == self.maxCoord[0] and outy == self.maxCoord[1]:
            return 0, 0
        if outx == self.minCoord[0] and outy == self.minCoord[1]:
            return 0, 1
        return outx, outy

    def buildEdges(self):
        out = ""
        count = 0
        for col in range(len(self.data)):
            for row in range(len(self.data[0])):
                if col > 0:
                    out += str(self.encode(col, row)) + " " + str(self.encode(col-1, row)) + " " + \
                           str(abs(self.data[col][row] - self.data[col-1][row]))
                    count += 1
                if row > 0:
                    out += str(self.encode(col, row)) + " " + str(self.encode(col, row-1)) + " " + \
                           str(abs(self.data[col][row] - self.data[col][row-1]))
                    count += 1
                if row < len(self.data[0])-1:
                    out += str(self.encode(col, row)) + " " + str(self.encode(col, row+1)) + " " + \
                           str(abs(self.data[col][row] - self.data[col][row+1]))
                    count += 1
                if col < len(self.data)-1:
                    out += str(self.encode(col, row)) + " " + str(self.encode(col+1, row)) + " " + \
                           str(abs(self.data[col][row] - self.data[col+1][row]))
                    count += 1
        out = str(count) + '\n' + str(len(self.data) * len(self.data[0])) + '\n' + out
        return out