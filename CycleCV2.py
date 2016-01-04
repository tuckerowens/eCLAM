

class CycleCV2:
    def __init__(self, filename):
        # Well now I guess I need to figure out how to reda this file...
        file = open(filename, 'r')
        self.filename = filename
        line = file.readline()
        self.metadata = list()
        while not "TABLE" in line:
            attr_array = line.split("\t")
            if len(attr_array) > 3:
                elements = {}
                elements["varname"] = attr_array[0]
                elements["type"] = attr_array[1]
                elements["data"] = attr_array[2]
                elements["name"] = attr_array[len(attr_array) - 1]
                self.metadata.append(elements)
            line = file.readline()

        temp_table = ""
        self.labels = file.readline().split("\t")
        self.datatypes = file.readline().split("\t")

        line = file.readline()
        while not "TABLE" in line:
            temp_table += line + '\n'
            line = file.readline()

        rows = temp_table.split("\n")
        #converts the data to 2D
        self.table = map(lambda x: x.split("\t"), rows)
        self.table = [i for i in self.table if len(i) > 1]

    def getDataAtPoint(self, point):
        return float(self.table[point][4])

    def getAllData(self):
        return list(map(lambda x: float(x[4]), self.table))

    def getVoltages(self):
        return list(map(lambda x: float(x[3]), self.table))

    def getTimes(self):
        return list(map(lambda x: float(x[2]), self.table))

    def print_labels(self):
        print (self.labels)


    def print_table(self):
        print (self.table)

